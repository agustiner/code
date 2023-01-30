# .bashrc

# User specific aliases and functions

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# I like color in my directory listing
alias ls='ls -F --color'

# Alias for the subnet command:
alias subnet='/afs/slac/g/scs/net/bin/subnet'


HOSTNAME=`hostname`
case $HOSTNAME in

"lcls-dev1" )
#    export EPICS_VER=3-14-12
     source /afs/slac/g/cd/swe/rhel5/tools/script/ENVS_swe.bash
     export JAVAVER=1.7.0_01
     export JAVA_HOME=/afs/slac/g/cd/swe/rhel5/package/java/jdk1.7.0_01
     export PATH=$JAVA_HOME/bin:$PATH
     export NETBEANS_HOME=/afs/slac/g/cd/swe/rhel5/package/netbeans/netbeans-7.0.1
     export PATH=$NETBEANS_HOME/bin:$PATH:/usr/afsws/bin

#    echo "Environment for Test Facility Development: RHEL5: 32-bit"
    ;;

"cecile-dev1" )
#    export EPICS_VER=3-14-12
     source /afs/slac/g/lcls/tools/script/ENVS.bash
     source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12.bash

#    echo "Environment for Test Facility Camera Development: RHEL5: 32-bit"
    ;;

"testfac-srv01" )
#     export EPICS_VER=3-14-12
      export ACCTEST_ROOT=/afs/slac/g/acctest
      source /afs/slac/g/acctest/tools/script/ENVS_acctest.bash
#     export JAVAVER=1.7.0_01
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.7.0_01
#     export JAVAVER=1.6.0_27
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.6.0_27
#     export JAVAVER=1.5.0_14
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.5.0_14
#     export PATH=$JAVA_HOME/bin:$PATH
#     export NETBEANS_HOME=/afs/slac/g/acctest/package/netbeans/netbeans-7.0.1
#     export PATH=$NETBEANS_HOME/bin:$PATH:/usr/afsws/bin

#    echo "Environment for Test Facility Production: RHEL5: 32-bit"
   ;;

"testfac-camsrv01" )
#     export EPICS_VER=3-14-12
      export ACCTEST_ROOT=/afs/slac/g/acctest
      source /afs/slac/g/acctest/tools/script/ENVS_acctest.bash
#     export JAVAVER=1.7.0_01
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.7.0_01
#     export JAVAVER=1.6.0_27
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.6.0_27
#     export JAVAVER=1.5.0_14
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.5.0_14
#     export PATH=$JAVA_HOME/bin:$PATH
#     export NETBEANS_HOME=/afs/slac/g/acctest/package/netbeans/netbeans-7.0.1
#     export PATH=$NETBEANS_HOME/bin:$PATH:/usr/afsws/bin

#    echo "Environment for Test Facility Production: RHEL5: 32-bit"
   ;;


"testfac-camsrv02" )
#     export EPICS_VER=3-14-12
      export ACCTEST_ROOT=/afs/slac/g/acctest
      source /afs/slac/g/acctest/tools/script/ENVS_acctest.bash
#     export JAVAVER=1.7.0_01
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.7.0_01
#     export JAVAVER=1.6.0_27
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.6.0_27
#     export JAVAVER=1.5.0_14
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.5.0_14
#     export PATH=$JAVA_HOME/bin:$PATH
#     export NETBEANS_HOME=/afs/slac/g/acctest/package/netbeans/netbeans-7.0.1
#     export PATH=$NETBEANS_HOME/bin:$PATH:/usr/afsws/bin

#    echo "Environment for Test Facility Production: RHEL5: 32-bit"
   ;;

"testfac-asta-cs01" )
#     export EPICS_VER=3-14-12
      export ACCTEST_ROOT=/afs/slac/g/acctest
      source /afs/slac/g/acctest/tools/script/ENVS_acctest.bash
#     export JAVAVER=1.7.0_01
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.7.0_01
#     export JAVAVER=1.6.0_27
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.6.0_27
#     export JAVAVER=1.5.0_14
#     export JAVA_HOME=/afs/slac/g/acctest/package/java/jdk1.5.0_14
#     export PATH=$JAVA_HOME/bin:$PATH
#     export NETBEANS_HOME=/afs/slac/g/acctest/package/netbeans/netbeans-7.0.1
#     export PATH=$NETBEANS_HOME/bin:$PATH:/usr/afsws/bin

#    echo "Environment for Test Facility Production: RHEL5: 32-bit"
   ;;


"cd-test2" )
#    export EPICS_VER=3-14-12
     source /afs/slac/g/lcls/tools/script/ENVS.bash
     # Setup JAVA and NETBEANS
     export JAVAVER=1.7.0_01
     source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12.bash
     export JAVA_HOME=/afs/slac/g/lcls/package/java/jdk1.7.0_01
     export PATH=$JAVA_HOME/bin:$PATH
     export NETBEANS_HOME=/afs/slac/g/lcls/package/netbeans/netbeans-7.0.1
     export PATH=$NETBEANS_HOME/bin:$PATH
     # Setup CSS
     export CSS_EPICS_VER=3.1.0
     export CSS_EPICS_HOME=/afs/slac/g/lcls/package/CSS/CSS_EPICS_$CSS_EPICS_VER
     export PATH=$CSS_EPICS_HOME:$PATH:/usr/afsws/bin

#    echo "Environment for LCLS 1 Development: RHEL4-32 is set"
    ;;

"lcls-dev2" )
#    export EPICS_VER=3-14-12
     source /afs/slac/g/lcls/tools/script/ENVS.bash
     # Setup JAVA and NETBEANS
     export JAVAVER=1.7.0_01
     source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12.bash
     export JAVA_HOME=/afs/slac/g/lcls/package/java/jdk1.7.0_01
     export PATH=$JAVA_HOME/bin:$PATH
     export NETBEANS_HOME=/afs/slac/g/lcls/package/netbeans/netbeans-7.0.1
     export PATH=$NETBEANS_HOME/bin:$PATH
     # Setup CSS
     export CSS_EPICS_VER=3.1.0    
     export CSS_EPICS_HOME=/afs/slac/g/lcls/package/CSS/CSS_EPICS_$CSS_EPICS_VER
     export PATH=$CSS_EPICS_HOME:$PATH:/usr/afsws/bin
     
#    echo "Environment for LCLS 1 Development: RHEL4-32 is set"
    ;;

"lcls-devcam01" )
#    export EPICS_VER=3-14-12
     source /afs/slac/g/lcls/tools/script/ENVS.bash
     # Setup JAVA and NETBEANS
     export JAVAVER=1.7.0_01
     source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12.bash
     export JAVA_HOME=/afs/slac/g/lcls/package/java/jdk1.7.0_01
     export PATH=$JAVA_HOME/bin:$PATH
     export NETBEANS_HOME=/afs/slac/g/lcls/package/netbeans/netbeans-7.0.1
     export PATH=$NETBEANS_HOME/bin:$PATH
     # Setup CSS
     export CSS_EPICS_VER=3.1.0
     export CSS_EPICS_HOME=/afs/slac/g/lcls/package/CSS/CSS_EPICS_$CSS_EPICS_VER
     export PATH=$CSS_EPICS_HOME:$PATH:/usr/afsws/bin

#    echo "Environment for LCLS 1 Development: RHEL4-32 is set"
    ;;

"lcls-devcam02" )
#    export EPICS_VER=3-14-12
     source /afs/slac/g/lcls/tools/script/ENVS.bash
     # Setup JAVA and NETBEANS
     export JAVAVER=1.7.0_01
     source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12.bash
     export JAVA_HOME=/afs/slac/g/lcls/package/java/jdk1.7.0_01
     export PATH=$JAVA_HOME/bin:$PATH
     export NETBEANS_HOME=/afs/slac/g/lcls/package/netbeans/netbeans-7.0.1
     export PATH=$NETBEANS_HOME/bin:$PATH
     # Setup CSS
     export CSS_EPICS_VER=3.1.0
     export CSS_EPICS_HOME=/afs/slac/g/lcls/package/CSS/CSS_EPICS_$CSS_EPICS_VER
     export PATH=$CSS_EPICS_HOME:$PATH:/usr/afsws/bin

#    echo "Environment for LCLS 1 Development: RHEL4-32 is set"
    ;;


"lcls-dev3" )
      source /afs/slac/g/lcls/tools/script/ENVS.bash
#      source /afs/slac/g/lcls/epics/setup/epicsenv-3.15.5-1.1.bash
      source /afs/slac/g/lcls/epics/setup/epicsenv-7.0.3.1-1.0.bash

    ;;

"aird-b50-srv01")
      source /afs/slac/g/lcls/tools/script/ENVS.bash
      source /afs/slac/g/lcls/epics/setup/epicsenv-7.0.3.1-1.0.bash
    ;;


"rdsrv300" )
#      source /afs/slac/g/lcls/tools/script/ENVS.bash
#      source /afs/slac/g/lcls/epics/setup/epicsenv-3.15.5-1.1.bash
#      source /afs/slac/g/lcls/epics/setup/epicsenv-7.0.3.1-1.0.bash

    ;;

"aird-pc90626" )
      source /afs/slac/g/lcls/tools/script/ENVS.bash
      source /afs/slac/g/lcls/epics/setup/epicsenv-3.15.5-1.1.bash
    ;;


*)
    if [ -f /afs/slac/g/lcls/tools/script/ENVS.bash ]; then
        source /afs/slac/g/lcls/tools/script/ENVS.bash
    fi
     source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12.bash
     export JAVA_HOME=/afs/slac/g/lcls/package/java/jdk1.7.0_01
     export PATH=$JAVA_HOME/bin:$PATH
     export NETBEANS_HOME=/afs/slac/g/lcls/package/netbeans/netbeans-7.0.1
     export PATH=$NETBEANS_HOME/bin:$PATH:/usr/afsws/bin

#    echo "Default Development Environment for RHEL4-32 is set"
#    echo "The same as lcls-dev2: Development for LCLS 1"
    ;;
esac


#export GIT_ROOT=/u/re/sgruden/work/git_repos
export GIT_ROOT=/afs/slac/g/cd/swe/git/repos

export TEST_STAND=/afs/slac/g/lcls/epics/TestStand
export TRAINING=/afs/slac/g/cd/swe/rhel5/epics/Training
export ASYN_CLASS=/afs/slac/g/cd/swe/rhel5/epics/Training/asynClass

# ==============================================================================
# Use newer version of GIT:
# ==============================================================================
# The version of git that ships and follows RHEL6 is out-dated.
# This causes problems when working with the EPICS core developers.
export PATH=/afs/slac/g/lcls/package/git/2.18.0/rhel6-x86_64/bin:$PATH
# ==============================================================================

# ==============================================================
# New Development Area:
# The following our new control systems development servers:
# lcls-dev2:  will be used for RHEL4 (32-bit OS)
# lcls-dev3:  will be used for RHEL6 (64-bit OS)
# lcls-dev1:  will be second RHEL5 (32-bit OS)
# ==============================================================

# Take me to RHEL6 (64-bit) EPICS Development
alias rhel6='source /afs/slac/g/cd/swe/rhel6/epics/setup/go_epics_3-14-12_swe_rhel6.bash'

# Take me to RHEL5 (32-bit) EPICS Development
alias rhel5='source /afs/slac/g/cd/swe/rhel5/epics/setup/go_epics_3-14-12_swe.bash'

# Take me to RHEL4 (32-bit) EPICS R3-14-12
alias dev2='source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12.bash'

# Make sure we put /bin and /usr/bin in front of /usr/local/bin
#export PATH=/bin:/usr/bin:$PATH

# CVS alias
alias cvs='cvs -d `echo $CVSROOT`'


# ACCL-VLAN Network Sniffers
#alias sniffer1='ssh root@172.31.75.126'
#alias sniffer2='ssh root@172.31.75.190'

# Where is my Documentation:
export DOCU=${EPICS_TOP}/Documentation


export PRINTER=hpslcprint

# =================================================================
# License Server for MATLAB 2007b
# =================================================================
export MLM_LICENSE_FILE=27010@sunlics1.slac.stanford.edu:27010@sunlics2.slac.stanford.edu:27010@sunlics3.slac.stanford.edu

# ===============================================================
# Setup for Xilinx -- Vivado  (RHEL64)===========================
# ===============================================================
export VIVADO_HOME=/nfs/slac/g/lcls/build/Xilinx/Vivado/2014.2
#source $VIVADO_HOME/settings64.sh
export PATH=$VIVADO_HOME/bin:$PATH

# ===================================================================
# License Server for Xilinx Vivado
# ===================================================================
export XILINXD_LICENSE_FILE=2100@license1:2100@license2:2100@license3


# ===============================================================
# Setup for vxWorks =============================================
# ===============================================================
#export LM_LICENSE_FILE=27006@sunlics1.slac.stanford.edu
#export WIND_HOME=/afs/slac/package/vxworks/devel/6.7
#sh /afs/slac/package/vxworks/devel/6.6/wrenv.sh -p vxworks-6.6

# Looks like I need the following on some versions of Linux.
# eval `/afs/slac/package/vxworks/devel/6.6/wrenv.sh -p vxworks-6.6 -o print_env -f sh`
#eval `/afs/slac/package/vxworks/devel/6.7/wrenv.sh -p vxworks-6.7 -o print_env -f sh`
#eval `/afs/slac/package/vxworks/devel/6.8/wrenv.sh -p vxworks-6.8 -o print_env -f sh`
#sh /afs/slac/package/vxworks/devel/6.7/wrenv.sh -p vxworks-6.7
#sh /afs/slac/package/vxworks/devel/6.8/wrenv.sh -p vxworks-6.8
# export WIND_LIC_PROXY=$WIND_HOME/setup/x86-linux2/bin/licproxy_3
# export PATH=$PATH:$WIND_HOME/setup/x86-linux2/bin
# ================================================================

# Alias to switch over to the new EPICS
#alias newepics='source /afs/slac/g/lcls/epics/setup/go_epics_3-14-12-4_1-0.bash'
alias newepics='source /afs/slac/g/lcls/epics/setup/go_epics_3.15.5-1.0.bash'
alias epics7='source /afs/slac/g/lcls/epics/setup/go_epics_7_devl.bash'

# ENV Variable for TFTP Server:
export TFTP_TOP=/afs/slac/g/lcls/tftpboot

# TOP for BuildRoot = linuxRT
export LINUX_RT=/afs/slac/package/linuxRT


# Disable CC cache
export CCACHE_DISABLE=1

#=================================================================================================
# Setup Python Version 2.7.9: Overide the default
# ================================================================================================
export PATH=$PACKAGE_TOP/python/python2.7.9/linux-x86_64/bin:$PATH
#export PYTHONPATH=<location to other libraries not in site-packages>
export LD_LIBRARY_PATH=$PACKAGE_TOP/python/python2.7.9/linux-x86_64/lib:$PACKAGE_TOP/python/python2.7.9/linux-x86_64/lib/python2.7/lib-dynload:$LD_LIBRARY_PATH
# ================================================================================================


# Prompt enhancement to show git branch names:
# ==============================================================================
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
# ==============================================================================

# ==============================================================================
# Use newer version of GIT:
# ==============================================================================
# The versions of git that ship and RHEL6/RHEL7 is out-dated.
# This causes problems when working with the EPICS core developers.
# ==============================================================================
export PATH=/afs/slac/g/lcls/package/git/2.18.0/rhel6-x86_64/bin:$PATH
# ==============================================================================

# ==============================================================================
# Git show tree in terminal
# ==============================================================================
alias gittree="git log --all --graph --decorate --oneline --simplify-by-decoration"
# ==============================================================================

