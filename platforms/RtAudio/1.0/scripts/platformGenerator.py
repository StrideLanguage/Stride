# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 08:29:07 2016

@author: andres
"""
from subprocess import check_output as ck_out
import platform
import shutil
import os
from strideplatform import GeneratorBase

from platformTemplates import templates # Perhaps we should acces this through PlatformFunctions ?

class Generator(GeneratorBase):
    def __init__(self, out_dir = '',
                 platform_dir = '',
                 debug = False):

        super(Generator, self).__init__(out_dir, platform_dir, debug)

        # TODO get gamma sources and build and install if not available
        # Question: building requires cmake, should binaries be distributed instead?
        # What about secondary deps like portaudio and libsndfile?
        self.log("Building RtAudio project")
        self.log("Buiding in directory: " + self.out_dir)

    def generate_code(self):
        # Generate code from tree
        # TODO These defaults should be set from the platform definition file
        self.block_size = 512
        self.sample_rate = 44100
        self.num_out_chnls = 2
        self.num_in_chnls = 2
        self.audio_device = -1

        self.log("Platform code generation starting...")

        domain = "AudioDomain"
        code = self.platform.generate_code(self.tree, domain)

        #var_declaration = ''.join(['double stream_%02i;\n'%i for i in range(stream_index)])
        #declare_code = var_declaration + declare_code


        filename = self.out_dir + "/main.cpp"
        shutil.copyfile(self.project_dir + "/template.cpp", filename)
        if os.path.isdir(self.out_dir + "/rtaudio"):
            shutil.rmtree(self.out_dir + "/rtaudio")
        shutil.copytree(self.project_dir + "/rtaudio-4.1.2", self.out_dir + "/rtaudio")

        self.write_code(code,filename)

        #print(str(domains))

        if platform.system() == "Linux":
            try:
                self.log("Running astyle...")
                ck_out(['astyle', self.out_file ])
            except:
                self.log("Error running astyle!")
        elif platform.system() == "Darwin":
            try:
                self.log("Running astyle...")
                ck_out(['/usr/local/bin/astyle', self.out_file ])
            except:
                self.log("Error running astyle!")
        else:
            self.log("Platform '%s' not supported!"%platform.system())


        self.link_flags = []
        for link_target in code['global_groups']['linkTo']:
            new_flag = "-l" + link_target
            if not new_flag in self.link_flags:
                self.link_flags.append(new_flag)

        for link_dir in code['global_groups']['linkDir']:
            new_flag = "-L" + link_dir
            if not new_flag in self.link_flags:
                self.link_flags.append(new_flag)

        self.build_flags = []
        for include_dir in code['global_groups']['includeDir']:
            new_flag = "-I" + include_dir
            if not new_flag in self.build_flags:
                self.build_flags.append(new_flag)

        self.build_flags.append("-I" + self.out_dir + "/rtaudio")

        self.log("Platform code generation finished!")

# Compile --------------------------
    def compile(self):

        self.log("Platform code compilation started...")

        import platform

        os.chdir(self.out_dir)

        if platform.system() == "Windows":

            source_files = [self.out_file, self.out_dir + "/rtaudio/RtAudio.cpp"]
            cpp_compiler = "c++"

            for f in source_files:
                short_f = f[f.rindex("/") + 1:]
                flags = ["-std=c++11",
                         "-I"+ self.platform_dir +"include",
                         "-O3",
                         "-DNDEBUG",
                         "-D__WINDOWS_WASAPI__",
                         "-Irtaudio/include"
                         "-o " + short_f + ".o",
                         "-c "+ f]

                args = [cpp_compiler] + flags

                outtext = ck_out(args)
                self.log(outtext)

            # Link ------------------------
            flags = ["-O3",
                     "-DNDEBUG",
                     "-D__WINDOWS_WASAPI__",
                     "-Irtaudio/include"]


            flags += [f[f.rindex("/") + 1:] + ".o" for f in source_files]
            flags += ["-o " + self.out_dir +"/app",
                     "-lole32",
                     "-lwinmm",
                     "-lksuser",
                     "-luuid"
                     ]

            args = [cpp_compiler] + flags

            outtext = ck_out(args)
            self.log(outtext)

        elif platform.system() == "Linux":

            source_files = [self.out_file, self.out_dir + "/rtaudio/RtAudio.cpp"]

            cpp_compiler = "/usr/bin/g++"

            pulse_defines = ['-D__LINUX_PULSE__']
            pulse_link_flags = ['-lpthread', '-lpulse-simple', '-lpulse']

            alsa_defines = ['-D__LINUX_ALSA__']
            alsa_link_flags = [ "-lasound", '-lpthread']

            module = 'pulse'

            if module == 'pulse':
                defines = pulse_defines
                link_flags = pulse_link_flags
            elif module == 'alsa':
                defines = alsa_defines
                link_flags = alsa_link_flags

            for f in source_files:
                short_f = f[f.rindex("/") + 1:]
                args = [cpp_compiler,
#                        "-I" + self.platform_dir + "/include",
                        "-I"+ self.out_dir + "/rtaudio",
                        "-O3" ,
                        "-std=c++11",
                        "-DNDEBUG"]
                args += defines
                args += ["-o" + short_f + ".o",
                         "-c",
                         f]

                self.log(args)

                outtext = ck_out(args)
                self.log(outtext)

             # Link ------------------------
            args = [cpp_compiler,
                    "-O3",
                    "-std=c++11",
                    "-DNDEBUG"
                    ]


            args += [f[f.rindex("/") + 1:] + ".o" for f in source_files]
            args += ["-o" + self.out_dir + "/app"]
            args += link_flags

            args += self.build_flags + self.link_flags

            self.log(args)

#            # ck_out didn't work properly on OS X
#            os.system(' '.join(args))
#
#
#
#            args = [cpp_compiler,
##                    "-I" + self.platform_dir + "/include",
#                    "-O3",
#                    "-std=c++11",
#                    "-I"+ self.out_dir + "/rtaudio",
#                    "-DNDEBUG",
#                    "-D__LINUX_ALSA__ ",
#                     "-o" + self.out_dir +"/app",
#                     self.out_file,
#                     self.out_dir + "/rtaudio/RtAudio.cpp",
#                     "-lasound",
#                     "-lpthread"
#                     ]
#
#            self.log(args)
            outtext = ck_out(args)

            self.log(outtext)


        elif platform.system() == "Darwin":

            source_files = [self.out_file, self.out_dir + "/rtaudio/RtAudio.cpp"]

            cpp_compiler = "/usr/bin/c++"

            for f in source_files:
                short_f = f[f.rindex("/") + 1:]
                args = [cpp_compiler,
                        "-I"+ self.out_dir + "/rtaudio",
                        "-O3" ,
                        "-std=c++11",
                        "-DNDEBUG",
                        "-D__MACOSX_CORE__",
                        "-Irtaudio",
                         "-o" + short_f + ".o",
                         "-c",
                         f]

                self.log(args)

                outtext = ck_out(args)
                self.log(outtext)

            # Link ------------------------
            args = [cpp_compiler,
                    "-O3",
                    "-std=c++11",
                    "-DNDEBUG",
                    "-isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.12.sdk",
                    "-Wl,-search_paths_first",
                    "-Wl,-headerpad_max_install_names"]


            args += [f[f.rindex("/") + 1:] + ".o" for f in source_files]
            args += ["-o" + self.out_dir + "/app",
                    "-framework CoreFoundation",
                    "-framework CoreAudio",
                    "-lpthread"
                    ]

            args += self.build_flags + self.link_flags

            self.log(args)

            # ck_out didn't work properly on OS X
            os.system(' '.join(args))

        else:
            self.log("Platform '%s' not supported!"%platform.system())

        self.log("Platform code compilation finished!")
