#!/bin/bash

import os
import shutil

inputs = [('010', 'get_started', 'Course goals'),
          ('015', 'conventions', 'Course conventions'),
          ('020', 'stages_hello_world', 'Stages of compilation & Hello, world'),
          ('030', 'types_and_ops', 'Variables, types, operators'),
          ('035', 'printing', 'Printing messages'),
          ('040', 'decisions', 'Decisions'),
          ('050', 'arrays', 'Arrays'),
          ('060', 'chars_strings', 'Characters & strings'),
          ('065', 'reading_input', 'Reading input'),
          ('070', 'command_line_args', 'Command line arguments'),
          ('080', 'assertions', 'Assertions'),
          ('090', 'math', 'Math'),
          ('100', 'compile_link', 'Compiling and linking'),
          ('110', 'functions', 'Functions'),
          ('120', 'program_structure', 'Program structure'),
          ('130', 'makefiles', 'Makefiles'),
          ('140', 'memory', 'Memory'),
          ('150', 'pointers', 'Pointers'),
          ('160', 'ptrs_arrays', 'Pointers & arrays'),
          ('170', 'lifetime_scope', 'Lifetime & scope'),
          ('180', 'stack_heap', 'Stack & heap'),
          ('190', 'dynamic_mem', 'Dynamic memory allocation'),
          ('200', 'valgrind', 'Debugging with valgrind'),
          ('210', 'gdb', 'Debugging with gdb'),
          ('220', 'structs', 'Structures'),
          ('230', 'beyond_1d', 'Beyond 1D arrays'),
          ('240', 'binary_io', 'Binary input/output'),
          ('250', 'numeric_types', 'Numeric types'),
          ('260', 'casting_promotion', 'Type casting & promotion'),
          ('270', 'bitwise_ops', 'Bitwise operators'),
          ('280', 'linked_lists', 'Linked lists, part 1'),
          ('290', 'linked_lists_2', 'Linked lists, part 2'),
          ('500', 'cpp_intro', 'C++ intro'),
          ('510', 'io_namespaces', 'C++ I/O and namespaces'),
          ('520', 'strings', 'C++ strings'),
          ('530', 'stl_intro', 'Standard Template Library (STL)'),
          ('540', 'vector_iter', 'STL vector & iterators'),
          ('550', 'map', 'STL map'),
          ('560', 'more_iterators', 'More about iterators'),
          ('570', 'pair_tuple', 'STL pairs and tuples'),
          ('580', 'references', 'References'),
          ('600', 'classes', 'Classes'),
          ('610', 'constructors', 'Constructors'),
          ('620', 'new_delete', 'new and delete'),
          ('630', 'non_default_ctors', 'Non-default constructors'),
          ('640', 'destructors', 'Destructors'),
          ('650', 'pass_by_ref', 'Passing by reference'),
          ('660', 'inheritance', 'Inheritance'),
          ('670', 'polymorphism', 'Polymorphism'),
          ('675', 'virt_dtors', 'Virtual destructors'),
          ('680', 'overloading', 'Overloading'),
          ('690', 'enum', 'Enumerations'),
          ('700', 'static_members', 'Static members'),
          ('710', 'design_principles', 'Object oriented design principles'),
          ('720', 'stringstream', 'Building strings with stringstream'),
          ('730', 'fstream', 'File I/O with fstream'),
          ('740', 'exceptions', 'Exceptions'),
          ('750', 'ruleof3', 'The Rule of 3'),
          ('760', 'template_funcs', 'Template functions'),
          ('770', 'template_classes', 'Template classes'),
          ('780', 'abstract_classes', 'Abstract classes'),
          ('790', 'writing_containers', 'Writing a container class'),
          ('800', 'auto', 'auto type'),
          ('810', 'ranged_for', 'ranged_for loops'),
          ('820', 'override', 'Override keyword')
          ]

if os.path.exists('full_set'):
	raise RuntimeError("full_set output dir already exists")

os.mkdir('full_set')

manifest = os.path.join('full_set', 'manifest.txt')
with open(manifest, 'wt') as manifest_fh:

	for num, short, long in inputs:
		combined = num + '_' + short
		input_pdf_name = short + '.pdf'
		input_pdf_path = os.path.join(combined, input_pdf_name)
		if not os.path.exists(input_pdf_path):
			raise RuntimeError('"%s" does not exist' % input_pdf_path)

		output_pdf_path = os.path.join('full_set', combined + '.pdf')
		shutil.copyfile(input_pdf_path, output_pdf_path)
		url = 'http://www.cs.jhu.edu/~langmea/resources/lecture_notes/' + combined + '.pdf'
		manifest_fh.write('\t'.join([combined, long, url]) + '\n')
