"""Optional pinned Linux dependency build; no system-wide installation or secrets."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sysconfig,tarfile,urllib.request
import numpy

REVISION='f302756b8af2b763db58e278e30478517dc8eea3'
GSL_SHA='6a99eeed15632c6354895b1dd542ed5a855c0f15d9ad1326c6fe2b2c9e423190'
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--patch',type=Path,default=ROOT.parent/'optional-agama/stable-angles.patch')
    a=p.parse_args();patch=a.patch.resolve()
    if not patch.is_file():raise SystemExit('Provide the released full stable-angles patch with --patch.')
    root=a.out.resolve()
    if any(c.isspace() for c in str(root)):raise SystemExit('Use a build directory without whitespace (Makefile paths).')
    root.mkdir(parents=True,exist_ok=False);os.nice(10)
    archive=root/'gsl-2.8.tar.gz'
    with urllib.request.urlopen('https://ftp.gnu.org/gnu/gsl/gsl-2.8.tar.gz',timeout=60) as response:
        archive.write_bytes(response.read())
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=GSL_SHA:raise RuntimeError('GSL archive checksum mismatch')
    with tarfile.open(archive) as source:source.extractall(root,filter='data')
    commands=[]
    def run(args,cwd,log,env=None):
        commands.append(args)
        with (root/log).open('w') as f:
            subprocess.run(args,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=1200)
    gsl=root/'gsl-local';env=os.environ.copy();env['CFLAGS']='-O2 -fPIC'
    run(['./configure','--prefix='+str(gsl),'--disable-shared'],root/'gsl-2.8','gsl-configure.log',env)
    run(['make','-j1'],root/'gsl-2.8','gsl-build.log')
    run(['make','install'],root/'gsl-2.8','gsl-install.log')
    run(['git','clone','https://github.com/GalacticDynamics-Oxford/Agama.git','Agama'],root,'clone.log')
    agama=root/'Agama';run(['git','checkout',REVISION],agama,'checkout.log')
    run(['git','apply',str(patch)],agama,'patch.log')
    text='CXX = c++\nLINK = c++\nAR = ar\nFC = gfortran\n'
    text+=f'COMPILE_FLAGS_ALL = -O2 -fPIC -std=c++11 -DNDEBUG -I{gsl}/include\n'
    text+=f'COMPILE_FLAGS_LIB = -DHAVE_PYTHON -I{sysconfig.get_path("include")} -I{numpy.get_include()}\n'
    text+=f'LINK_FLAGS_ALL = -L{gsl}/lib\nLINK_FLAGS_LIB =\nLINK_FLAGS_LIB_AND_EXE_STATIC = -lgsl -lgslcblas -lm\n'
    (agama/'Makefile.local').write_text(text);run(['make','-j1','lib'],agama,'agama-build.log')
    result=dict(agama_revision=REVISION,gsl_version='2.8',gsl_archive_sha256=GSL_SHA,
                patch_sha256=hashlib.sha256(patch.read_bytes()).hexdigest(),
                library_sha256=hashlib.sha256((agama/'agama.so').read_bytes()).hexdigest(),
                build_recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='Pinned source dependency build. This alone is not a coordinate or scientific verification.')
    (root/'dependency-build.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
