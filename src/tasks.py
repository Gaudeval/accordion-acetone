"""
 *******************************************************************************
 * ACETONE: Predictable programming framework for ML applications in safety-critical systems
 * Copyright (c) 2022. ONERA
 * This file is part of ACETONE
 *
 * ACETONE is free software ;
 * you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation ;
 * either version 3 of  the License, or (at your option) any later version.
 *
 * ACETONE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY ;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License along with this program ;
 * if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
 ******************************************************************************
"""

from invoke import task
import platform
import os
@task
def clean(c):
    if platform.system()=='Windows':
        c.run("powershell rm -Recurse -Force ..\\output")
        c.run("powershell rm -Recurse -Force ..\\data\\example")
    elif platform.system()=='Linux':
        c.run("rm -Rf ../output")
        c.run("rm -Rf ../data/example")

@task(clean)
def init(c):
    c.run('python3 ../init/initial_setup.py')

@task(init)
def gen(c):
    command = "python3.12 -m acetone.cli_codegen"
    model = "../data/example/lenet5.json"
    inp = "../data/example/test_input_lenet5.txt"
    function = "lenet5"
    iterations = "1"
    version = "{{vx}}"
    output = "../output/acetone/example/"+version
    args= [command,model,inp,function,iterations,version,output]
    for i in range(1,8):
      c.run('mkdir -p '+output.replace('{{vx}}','v'+str(i)))
      c.run(' '.join(args).replace('{{vx}}','v'+str(i)))

@task(gen)
def build(c):
    for i in range(1,3):
      path = os.getcwd()+'/../output/acetone/example/v'+str(i)
      c.run('make -C '+os.path.abspath(path))
      c.run(os.path.abspath(path+'/lenet5')+' '+os.path.abspath(path+'/log.txt'))

@task(build)
def all(c):
    pass
