#!/usr/bin/env python

"""
Script that takes a cppmd file (Markdown with inline C/C++), runs the
appropriate commands to compile and run the C/C++, does ppropriate
substitutions so commands and output appear, outputs markdown, then
runs pandoc to convert final markdown into slides.

Brief specification for cppmd files
===================================

File blocks
-----------

Blocks set off with <!---cppmd-file ... --> contain the contents of a text
file, usually source code.  Example:

<!---cppmd-cppfile unit7_headers1.cpp
#include <iostream>

int main(void) {
	std::cout << "Hello world" << std::endl;
	return 0;
}
-->

The name of the file is specified on the same line as the
"<!---cppmd-cppfile", separated by a space.

The "<!---cppmd-shell" has to be the first token on the line.

The contents of the file are also echoed into the final Markdown as C++
source, i.e. between "```cpp" and "```" lines.

Shell blocks
------------

Blocks set off with <!---cppmd-shell ... --> contain shell code to run.
Example:

<!---cppmd-shell
g++ -std=c++11 -pedantic -Wall -Wextra -o unit7_headers1 unit7_headers1.cpp
./unit7_headers1
-->

The "<!---cppmd-shell" has to be the first token on the line.

The commands themselves are printed into the final Markdown, with "$ "
prepended.  Standard out and standard error are also printed (with nothing
prepended).

"""

from __future__ import print_function

import os
import sys
import subprocess
import argparse
import textwrap

__author__ = "Ben Langmead"
__email__ = "ben.langmead@gmail.com"


def prefixize(st, pref):
    return pref + ' ' + st.replace('\n', '\n%s ' % pref)


def wrap(st):
    return '\n'.join(textwrap.wrap(st, 70, replace_whitespace=False)) + '\n' 


def handle_shell_commands(fh, ofh, last_source_file=None, no_echo=False, no_console=False, prefix='$ '):
    """
    Handle a block of shell commands.  First echo the command with "$ "
    prepended.  Then run the command and paste its output.  If there is stderr
    output, or if the input file is not formatted as expected, raise
    RuntimeError.

    :param prefix: prepend this when printing a command
    :param ofh: Output md file
    :param fh: Input cppmd file
    """
    if not no_echo:
        ofh.write("```\n")
    while True:
        ln = fh.readline()
        if len(ln) == 0:
            raise RuntimeError('Ended in the middle of a shell block')
        if ln.startswith('-->'):
            break
        ln = ln.rstrip()
        if '%PREV%' in ln:
            assert last_source_file is not None
            ln = ln.replace('%PREV%', last_source_file)
        if '%PREVBASE%' in ln:
            assert last_source_file is not None
            ln = ln.replace('%PREVBASE%', last_source_file[:last_source_file.rfind('.')])
        print('Running command "%s"' % ln, file=sys.stderr)
        if not no_echo:
            ofh.write(prefix + ln + '\n')
        p = subprocess.Popen(ln, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if not no_console:
            if len(out.rstrip()) > 0:
                print(prefixize(out.rstrip(), 'O:'))
            if len(err.rstrip()) > 0:
                print(prefixize(err.rstrip(), 'E:'))
        if not no_echo:
            if len(out) > 0:
                ofh.write(wrap(out.rstrip()))
            if len(err) > 0:
                ofh.write(wrap(err.rstrip()))
    if not no_echo:
        ofh.write("```\n")


def handle_source_file(fh, ofh, fn, no_echo=False, force=False, append=False):
    """
    Handle a file block.  Write the contents to a file with the specified name
    and echo to the markdown inside a ```cpp ... ``` block.

    :param fh: Input cppmd file
    :param ofh: Output md file
    :param fn: Name of output file
    :param force: If false, raise error when file with that name exists
    """
    if os.path.exists(fn) and not force:
        raise RuntimeError('Refusing to overwrite "%s"' % fn)
    if not no_echo:
        ofh.write("```cpp\n")
    to_echo = []
    with open(fn, 'a' if append else 'w') as cpp_ofh:
        while True:
            ln = fh.readline()
            if len(ln) == 0:
                raise RuntimeError('Ended in the middle of a C++ source block')
            if ln.startswith('-->'):
                break
            if not no_echo:
                to_echo.append(ln)
            if ln.startswith('//%ST%'):
                to_echo = []
            cpp_ofh.write(ln)
    if not no_echo:
        for ln in to_echo:
            ofh.write(wrap(ln))
        ofh.write("```\n")


def update_gitignore(fns):
    ignored = set()
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as fh:
            for ln in fh:
                ignored.add(ln.rstrip())
    if not ignored.issuperset(fns):
        ignored.update(fns)
        with open('.gitignore', 'w') as fh:
            for ig in ignored:
                fh.write(ig + '\n')


def go(fh, prefix, force, no_pandoc, beamer_theme=None, skip_gitignore=False):
    """
    Main driver.

    :param fh: Input file
    :param prefix: String to prepend to output files
    :param force: If false, raise error when about to overwtite a file
    :param no_pandoc: If true, skip running pandoc
    :param pandoc_style: Specifies style to pass to pandoc -t
    :return:
    """
    last_source_file = None
    fns = set()  # all generated files
    with open(prefix + '.md', 'w') as md_ofh:
        while True:
            ln = fh.readline()
            if len(ln) == 0:
                break
            if ln.strip().startswith('<!---cppmd-file'):
                skip = 'skip' in ln.rstrip().split()
                fn = ln.rstrip().split()[-1]  # file to create
                if not skip and not fn.endswith('.h'):
                    last_source_file = fn  # remember last .c/.cpp file

                # no-echo mode: for including source code in cppmd that
                # doesn't actually get rendered in slides
                no_echo = 'no-echo' in ln.rstrip().split()

                # append mode: for breaking up source over many slides
                append = 'append' in ln.rstrip().split()

                fns.add(fn)
                handle_source_file(fh, md_ofh, fn, force=force, no_echo=no_echo, append=append)
            elif ln.strip().startswith('<!---cppmd-shell'):

                # no-echo mode: for shell code that should not be rendered in
                # slides
                no_echo = ln.rstrip().split()[-1] == 'no-echo'

                handle_shell_commands(fh, md_ofh, last_source_file=last_source_file, no_echo=no_echo)
            else:
                md_ofh.write(ln)

    if not no_pandoc:
        if beamer_theme is not None:
            beamer_theme = '-V theme:' + beamer_theme + ' '
        cmd = 'pandoc -t %s %s%s -o %s' % ('beamer', beamer_theme, prefix + '.md', prefix + '.pdf')
        print('Running pandoc command: "%s"' % cmd, file=sys.stderr)
        os.system(cmd)

    if not skip_gitignore:
        update_gitignore(fns)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run a runnable C/C++ markdown file (.cppmd).  Create '
                    'source files (<!---cppmd-file (code) -->) '
                    'run shell commands (<!---cppmd-shell (code) -->) '
                    'and paste their output into the slides appropriately.'
                    'pandoc must be installed')
    parser.add_argument(
        '--prefix', metavar='path', type=str, required=True,
        help='Write output to <prefix>.md and <prefix>.pdf')
    parser.add_argument(
        '--beamer-theme', metavar='theme', type=str, required=True,
        help='Apply this beamer theme to all slides')
    parser.add_argument(
        '--force', action='store_const', const=True, default=False,
        help='Overwrite .c/.cpp files that already exist')
    parser.add_argument(
        '--skip-pandoc', action='store_const', const=True, default=False,
        help='Don\'t run pandoc; just write the <prefix>.md file')
    parser.add_argument(
        '--dont-update-gitignore', action='store_const', const=True, default=False,
        help='By default, .gitignore is updated to ignore files generated with '
             '<!---cppmd-file (code) -->.  This disables that behavior.')
    args = parser.parse_args()
    go(sys.stdin, args.prefix,
       force=args.force,
       no_pandoc=args.skip_pandoc,
       beamer_theme=args.beamer_theme,
       skip_gitignore=args.dont_update_gitignore)
