// Prescribed isochrone + rotating quadrupole. No self-gravity or collisions.
#include <cmath>
#include <vector>

struct Frame { double c, s, omega, amplitude; };

static double energy(double jr, double jz, double js) {
    const double L=jz+2*js, I=jr+.5*(L+std::sqrt(L*L+2));
    return -.5/(I*I);
}

static Frame frame(double t, const double* p) {
    // p = amplitude, fixed Jr/Jz defining the prescribed resonance, Js0, dJsres/dt.
    const double L=p[2]+2*(p[3]+p[4]*t), root=std::sqrt(L*L+2);
    const double I=p[1]+.5*(L+root), omega=.5*(1+L/root)/(I*I*I);
    const double angle=p[4]==0 ? omega*t : (energy(p[1],p[2],p[3]+p[4]*t)-energy(p[1],p[2],p[3]))/(2*p[4]);
    return {std::cos(2*angle),std::sin(2*angle),omega,p[0]};
}

static inline void field(const double* z, const Frame& f, double* out) {
    const double x=z[0],y=z[1],zz=z[2],r2=x*x+y*y+zz*zz;
    const double r=std::sqrt(r2),u=std::sqrt(.25+r2),den=.5+u;
    const double bg=-1/(u*den*den);
    const double q=(x*x-y*y)*f.c+2*x*y*f.s;
    const double ratio=1.28/(.28+r/.34),ratio2=ratio*ratio;
    const double C=-f.amplitude*.42*.42/(2*.34*.34)*ratio2*ratio2*ratio;
    const double radial=r>0 ? -5*C*q/((.28*.34+r)*r) : 0.;
    const double torque=2*C*(2*x*y*f.c-(x*x-y*y)*f.s);
    out[0]=-1/den+C*q;
    out[1]=bg*x-C*(2*x*f.c+2*y*f.s)-radial*x;
    out[2]=bg*y-C*(-2*y*f.c+2*x*f.s)-radial*y;
    out[3]=bg*zz-radial*zz;
    out[4]=f.omega*torque;out[5]=torque;
}

extern "C" void evaluate(const double* states,int n,double t,const double* p,double* out) {
    const Frame f=frame(t,p);
    for(int i=0;i<n;i++)field(states+6*i,f,out+6*i);
}

extern "C" void evolve(double* states,int n,int steps,double t0,double dt,
                       const double* p,double* torque,double* work) {
    std::vector<double> previous(6*n);
    evaluate(states,n,t0,p,previous.data());
    for(int k=0;k<steps;k++) {
        const Frame f=frame(t0+(k+1)*dt,p);
        for(int i=0;i<n;i++) {
            double* z=states+6*i;double* old=previous.data()+6*i;
            for(int d=0;d<3;d++){z[3+d]+=.5*dt*old[1+d];z[d]+=dt*z[3+d];}
            double now[6];field(z,f,now);
            for(int d=0;d<3;d++)z[3+d]+=.5*dt*now[1+d];
            torque[i]+=.5*dt*(old[5]+now[5]);work[i]+=.5*dt*(old[4]+now[4]);
            for(int d=0;d<6;d++)old[d]=now[d];
        }
    }
}
