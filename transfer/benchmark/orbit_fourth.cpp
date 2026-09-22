// Independent fourth-order composition; the original leapfrog stays unchanged.
#include "orbit_kernel.cpp"

extern "C" void evolve_fourth(double* states,int n,int steps,double t0,double dt,
                              const double* p,double* torque,double* work) {
    const double w1=1/(2-std::cbrt(2.0)), w0=1-2*w1;
    const double w[3]={w1,w0,w1};
    std::vector<double> previous(6*n);
    evaluate(states,n,t0,p,previous.data());
    for(int k=0;k<steps;k++) {
        double t=t0+k*dt;
        for(int q=0;q<3;q++) {
            const double h=w[q]*dt;
            const Frame f1=frame(t+h,p);
            for(int i=0;i<n;i++) {
                double* z=states+6*i;double* old=previous.data()+6*i;double now[6];
                for(int d=0;d<3;d++){z[3+d]+=.5*h*old[1+d];z[d]+=h*z[3+d];}
                field(z,f1,now);
                for(int d=0;d<3;d++)z[3+d]+=.5*h*now[1+d];
                torque[i]+=.5*h*(old[5]+now[5]);work[i]+=.5*h*(old[4]+now[4]);
                for(int d=0;d<6;d++)old[d]=now[d];
            }
            t+=h;
        }
    }
}
