This artifact corresponds to the ECRTS'22 paper paper "ACETONE: Predictable programming framework for ML applications in safety-critical systems".
It aims to reproduce the experiments done to verify the semantic preservation (see Sections 4.2 and 5) of the C code generated both by Keras2C and ACETONE frameworks for a given neural network model. 
First, a minimal reproducible example is created. Then, instructions are given so some of the results of the paper can be verified. 

I) INSTALLATION (for Linux OS)
------------------------------

(a) Install Docker following the instructions at https://docs.docker.com/get-docker/

(b) Once Docker is installed, download artifact_ecrts22_2_codegen.tar.gz image.

(c) Load the artifact_ecrts22_2_codegen image by typing the following command in the directory where the tar.gz file was downloaded:

$ docker load < artifact_ecrts22_2_codegen.tar.gz

(d) Run the docker image and start a bash session inside the docker by typing the following command:

$ docker run -v [PATH_SHARED]:/home/NNCodeGenerator/shared --name artifact_ecrts22_2_codegen_bash -i -t artifact_ecrts22_2_codegen bash

where PATH_SHARED is the folder of your host machine that will be shared with the docker container. 
The result files can be stored in this shared folder.
    
NOTE 1: to exit the Docker container simply type exit. To restart it simply do
$ docker restart aec_ecrts22_paper36_codegen_bash

II) CODE ORGANIZATION
---------------------

In the home directory there are a few files regarding the license and copyright information of the present artifact, to know:
- AUTHORS.txt
- COPYING.txt
- LICENSE.txt

The home directory contains as well the file "requirements.txt" with the precisions about packages versioning used in the Python environment.

Inside the directory NNCodeGenerator of the Docker container there are five folders:
- init, which contains the programs that allow creating an example neural network model and test files;
- data, which contains the generated test files used as input for the frameworks;
- framework, which contains Keras2C and ACETONE backend codes;
- output, which will contain the generated C code by both frameworks;
- shared, which will contain the files to be shared with host machine.

III) MINIMAL REPRODUCIBLE EXAMPLE
---------------------------------

The following sequence of commands allows to generate the C code corresponding to the LeNet-5 neural network architecture with both Keras2C and our framework (namely ACETONE),
execute one inference and compare the results.

III.1. Generate a neural network example model

First, go to the init directory:
$ cd NNCodeGenerator/init/

And execute the following command :
$ python3 initial_setup.py

This script first defines a model reproducing the Lenet-5 architecture, using the training framework Keras.
Afterward it saves this description in both h5 and JSON formats, which will be used as input for Keras2C and our framework, respectively.
To convert the recently created model, which is a Keras' object, to JSON format, we use a function defined by us. 
It also generates a random input that will be used to perform one single inference within all the frameworks.
Finally, this script prints and saves the result obtained when doing one forward-pass using the given input with the Keras framework, which will be our reference.
Please note that this generated model was not trained, i.e., the weights and biases are randomly initialized values. That is not harmful as for this example we are interested in verifying that the forward-pass executes correctly.

Go back to /home/NNCodeGenerator/ :
$ cd ..

III.2. C code generation with Keras2C:

In order to generate the C code for the model reproducing the LeNet-5 architecture with Keras2C, compile and execute it, use the following commands:

	a) First, go to the Keras2C framework directory:
	   $ cd framework/keras2c

	b) Call Keras2C backend passing as arguments the h5 file, the name to be given to the generated function, the file with the test input and the number of inferences to be performed (one in this case):
        $ python3 -m keras2c ../../data/example/lenet5.h5 lenet5 ../../data/example/test_input_lenet5.txt -t 1

	c) Compile the generated source code:
	   $ gcc -std=c99 -I./include/ -o lenet5 lenet5.c lenet5_test_suite.c -L./include/ -l:libkeras2c.a -lm
	
	d) Execute the generated file:
	   $ ./lenet5

	e) Move generated files to output directory so they can be easily found later:
        $ mv lenet5 lenet5.c lenet5.h lenet5_test_suite.c ../../output/keras2c/example/
	
	f) Go back to /home/NNCodeGenerator/ :
		$ cd ../..

III.3. C code generation with ACETONE:

Afterward, we can do the same experiment with our framework, for each one of the three versions. For the first version, follow:

	a) First, go to the directory where is located ACETONE framework:
	   $ cd framework/acetone
	
    b) Call ACETONE passing as arguments the JSON file describing the model, the file with the test input, the name of the generated function, the number of inferences to be performed (one in this case), the type of the generated code (versions) and the directory where generated code will be stored:
	   $ python3 main.py ../../data/example/lenet5.json ../../data/example/test_input_lenet5.txt  lenet5  1  v1 ../../output/acetone/example/v1

	c) Compile the code. Please note that the paranthesis in the following command are important so we don't switch directories for the compilation.
		$ ( cd ../../output/acetone/example/v1 && make )  

	d) Execute the generated file. The inference result will be printed and also exported to a text file.
        $ ( cd ../../output/acetone/example/v1 && ./lenet5 output_acetone.txt ) 

	e) Run the following command to compare the predictions of ACETONE and Keras:
		$ python3 eval_semantic_preservation.py ../../output/acetone/example/v1/output_acetone.txt ../../data/example/output_keras.txt 1

Same is done for the other two versions of our framework. For version 2, do:

	$ python3 main.py ../../data/example/lenet5.json ../../data/example/test_input_lenet5.txt  lenet5  1  v2 ../../output/acetone/example/v2
	$ ( cd ../../output/acetone/example/v2 && make )
	$ ( cd ../../output/acetone/example/v2 && ./lenet5 output_acetone.txt )
	$ python3 eval_semantic_preservation.py ../../output/acetone/example/v2/output_acetone.txt ../../data/example/output_keras.txt 1

Equally, for version 3, follow: 

	$ python3 main.py ../../data/example/lenet5.json ../../data/example/test_input_lenet5.txt  lenet5  1  v3 ../../output/acetone/example/v3	
	$ ( cd ../../output/acetone/example/v3 && make )
	$ ( cd ../../output/acetone/example/v3 && ./lenet5 output_acetone.txt )
	$ python3 eval_semantic_preservation.py ../../output/acetone/example/v3/output_acetone.txt ../../data/example/output_keras.txt 1

NOTE 2: the code of version 3 takes a little longer to be compiled.

V) REPRODUCTION OF PAPER'S EXPERIMENTS
--------------------------------------

V.1. Semantic preservation of C code generated with Keras2C:

In order to reproduce the results for semantic preservation for model acas_decr128, present in Table 1, use the following commands:
	$ cd framework/keras2c
	$ python3 -m keras2c ../../data/acas_decr128/acas_decr128.h5 acas_decr128 ../../data/acas_decr128/test_input_acas_decr128.txt -t 1000
	$ gcc -std=c99 -I./include/ -o acas_decr128 acas_decr128.c acas_decr128_test_suite.c -L./include/ -l:libkeras2c.a -lm
	$ ./acas_decr128
	$ mv acas_decr128 acas_decr128.c acas_decr128.h acas_decr128_test_suite.c ../../output/keras2c/acas_decr128/

Similarly, to reproduce the results for semantic preservation for the trained LeNet-5 model, also present in Table 1, use the following commands:
	
	$ python3 -m keras2c ../../data/lenet5_trained/lenet5_trained.h5 lenet5_trained ../../data/lenet5_trained/test_input_lenet5_trained.txt -t 1000
	$ gcc -std=c99 -I./include/ -o lenet5_trained lenet5_trained.c lenet5_trained_test_suite.c -L./include/ -l:libkeras2c.a -lm
	$ ./lenet5_trained
	$ mv lenet5_trained lenet5_trained.c lenet5_trained.h lenet5_trained_test_suite.c ../../output/keras2c/lenet5_trained/

Leave the Keras2C directory:
	
	$ cd ..

V.2. Semantic preservation of C code generated with ACETONE:

To reproduce the results for semantic preservation for model acas_decr128, now with our framework, use the following commands:
	
	$ cd acetone
	$ python3 main.py ../../data/acas_decr128/acas_decr128.json ../../data/acas_decr128/test_input_acas_decr128.txt  acas_decr128  1000  v1 ../../output/acetone/acas_decr128/v1	
	$ ( cd ../../output/acetone/acas_decr128/v1 && make )
	$ ( cd ../../output/acetone/acas_decr128/v1 && ./acas_decr128 output_acetone.txt )
	$ python3 eval_semantic_preservation.py ../../output/acetone/acas_decr128/v1/output_acetone.txt ../../data/acas_decr128/output_keras.txt 1000

Same can be done to obtain the results for semantic preservation for the trained LeNet-5 model:

	$ python3 main.py ../../data/lenet5_trained/lenet5_trained.json ../../data/lenet5_trained/test_input_lenet5_trained.txt  lenet5_trained  1000  v1 ../../output/acetone/lenet5_trained/v1	
	$ ( cd ../../output/acetone/lenet5_trained/v1 && make )
	$ ( cd ../../output/acetone/lenet5_trained/v1 && ./lenet5_trained output_acetone.txt )
	$ python3 eval_semantic_preservation.py ../../output/acetone/lenet5_trained/v1/output_acetone.txt ../../data/lenet5_trained/output_keras.txt 1000


Copy all the generated C code to the shared folder for deeper investigation:

$ cd ../..
$ cp -r ./output/ ./shared/


VI) GENERAL INFORMATION
-----------------------
NOTE 3: Output of Keras2C framework help:
$ python3 -m keras2c -h 
usage: keras2c [-h] [-m] [-t] model_path function_name test_dataset_path 

A library for converting the forward pass (inference) part of a keras model to a C function

positional arguments:
model_path         File path to saved keras .h5 model file
function_name      What to name the resulting C function
test_dataset_path  File path to testing inputs

optional arguments:
-h, --help         show this help message and exit
-m, --malloc       Use dynamic memory for large arrays. Weights will be saved to .csv files that will be loaded at runtime
-t , --num_tests   Number of tests to generate. Default is 10

NOTE 4: Output of the ACETONE framework help:
$ python3 main.py -h
usage: main.py [-h] model_file test_dataset_file function_name nb_tests version output_dir

C code generator for Neural Networks 

positional arguments:
  model_file         Input file that describes the neural network model
  test_dataset_file  Input file that contains test data				  
  function_name      Name of the generated function				  
  nb_tests           Number of inferences process to run
  version            Version to be used for the code generation
  output_dir         Output directory where generated files will be written

optional arguments:
-h, --help         show this help message and exit

