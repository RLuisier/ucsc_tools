#!/usr/bin/env python
import os
from distutils.cmd import Command
from distutils.core import setup
from distutils.sysconfig import get_config_vars
from distutils.command.install import install

class uninstall_scripts (Command):

    description = "install scripts (Python or otherwise)"

    user_options = [
        ('prefix=',None,'installation prefix'),
        ('install-dir=', 'd', "directory to install scripts to"),
        ('build-dir=','b', "build directory (where to install from)"),
        ('force', 'f', "force installation (overwrite existing files)"),
        ('skip-build', None, "skip the build steps"),
    ]

    boolean_options = ['force', 'skip-build']


    def initialize_options (self):
        self.prefix = None
        self.install_dir = None
        self.force = 0
        self.build_dir = None
        self.skip_build = None

    def finalize_options (self):
        self.set_undefined_options('install',
                                   ('install_scripts', 'install_dir'),
                                   ('prefix','prefix'),
                                   ('force', 'force'),
                                   ('skip_build', 'skip_build'),
                                  )
        self.install_dir = os.path.normpath(os.path.expanduser(self.prefix))
        self.install_dir = os.path.join(self.install_dir,'bin')

    def run (self):
        # delete scripts
        for script in self.distribution.scripts :
            self.remove_path(os.path.basename(script))

    def remove_path(self,path) :
        '''Attempt to remove the specified path, returning non-zero status code on error'''
        try :
            abs_path = os.path.abspath(os.path.join(self.install_dir,path))
            os.remove(abs_path)
            print 'rm %s'%os.path.join(self.install_dir,path)
        except Exception, e :
            print e

        #self.outfiles = self.copy_tree(self.build_dir, self.install_dir)
        #if os.name == 'posix':
            # Set the executable bits (owner, group, and world) on
            # all the scripts we just installed.
        #    for file in self.get_outputs():
        #        if self.dry_run:
        #            log.info("changing mode of %s", file)
        #        else:
        #            mode = ((os.stat(file)[ST_MODE]) | 0555) & 07777
        #            log.info("changing mode of %s to %o", file, mode)
        #            os.chmod(file, mode)

    def get_inputs (self):
        return self.distribution.scripts or []

    def get_outputs(self):
        return self.outfiles or []


#TODO this doesn't work yet - consider doing this later, use the install 
# -f|--force option for now

# distutils doesn't handle uninstalling things, this class deletes all the files
# this package installs if it has appropriate permissions to do it, otherwise
# print out the files that must be deleted to uninstall
class uninstall(install) :
  user_options = [
      # Select installation scheme and set base director(y|ies)
      ('prefix=', None,
       "installation prefix"),
      ]

  boolean_options = []
  negative_opt = {}

  # 'sub_commands': a list of commands this command might have to run to
  # get its work done.  See cmd.py for more info.
  #sub_commands = [('install_lib',     has_lib),
  #                ('install_headers', has_headers),
  #                ('install_scripts', has_scripts),
  #                ('install_data',    has_data),
  #                ('install_egg_info', lambda self:True),
  #               ]
  sub_commands = []

  def initialize_options(self) :
    self.prefix = None
    install.initialize_options(self)

  def run(self) :

    #print self.distribution.find_config_files()
    print self.distribution.command_options
    self.distribution.parse_config_files()
    print self.prefix
    print self.get_sub_commands()
    print self.__dict__
    print get_config_vars('prefix')

    # delete scripts
    for script in self.distribution.scripts :
        self.remove_path(os.path.basename(script))

  def remove_path(self,path) :
    '''Attempt to remove the specified path, returning non-zero status code on error'''
    try :
        abs_path = os.path.abspath(os.path.join(self.install_scripts,path))
        print 'rm %s'%os.path.join(self.install_scripts,path)
        #os.remove(abs_path)
    except Exception, e :
        print e



ucsc_executables = ["executables/bedClip",
          "executables/bedExtendRanges",
          "executables/bedGraphToBigWig",
          "executables/bedItemOverlapCount",
          "executables/bedSort",
          "executables/bedToBigBed",
          "executables/bigBedInfo",
          "executables/bigBedSummary",
          "executables/bigBedToBed",
          "executables/bigWigInfo",
          "executables/bigWigSummary",
          "executables/bigWigToBedGraph",
          "executables/bigWigToWig",
          "executables/faCount",
          "executables/faFrag",
          "executables/faOneRecord",
          "executables/faRandomize",
          "executables/faSize",
          "executables/faSomeRecords",
          "executables/faToNib",
          "executables/faToTwoBit",
          "executables/fetchChromSizes",
          "executables/fetch_executables.sh",
          "executables/gtfToGenePred",
          "executables/htmlCheck",
          "executables/liftOver",
          "executables/liftOverMerge",
          "executables/liftUp",
          "executables/mafsInRegion",
          "executables/mafSpeciesSubset",
          "executables/nibFrag",
          "executables/pslCDnaFilter",
          "executables/stringify",
          "executables/textHistogram",
          "executables/twoBitInfo",
          "executables/twoBitToFa",
          "executables/validateFiles",
          "executables/wigCorrelate",
          "executables/wigToBigWig"]

python_scripts = []

scripts = ucsc_executables + python_scripts

setup(name='UCSC Tools Wappers',
      version='0.0',
      scripts=scripts,
      cmdclass={'uninstall': uninstall_scripts},
     )
