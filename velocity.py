#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *
from sigma import sigma
from libzhang import *
from grid import grid

class vel:

    def __init__(self,m=0,N=0,n=1,l=None,nr=33,np=256,nt=128,symm='es'):

        n = n-1   # The definition of n starts from 1 :(
        N = (l - m - ((l-m)%2))/2

        self.grid = grid(nr=nr,np=np,nt=nt)
        self.Us = zeros([np,nt,nr])
        self.Up = zeros([np,nt,nr])
        self.Uz = zeros([np,nt,nr])

        sig_arr = sigma(m=m,N=N,l=l,symm=symm)
        print 'omega =',sig_arr*2
        sig = sig_arr[n]

        print 'omega(%d,%d,%d) = %.4f' %(l,m,n+1,sig*2)


        if l is not None:
			if (l-m)%2 == 0:
				symm = 'es'
			else:
				symm = 'ea'

        if (symm == 'es') or (symm == 'ES'):
        
            for i in range(N+1):
                for j in range(N-i+1):
                    C = (-1)**(i+j) * dfactorial(2*(m+N+i+j)-1)/  \
                        ( 2**(j+1) * dfactorial(2*i-1) * factorial(N-i-j)  \
                        * factorial(i) * factorial(j) * factorial(m+j) )
                    
                    if i > 0:

                        UTemp = C * sig**(2*i-1) * ( 1 - sig**2)**j * 2*i * \
                                self.grid.s3D**(m+2*j) * self.grid.z3D**(2*i-1)

                        self.Uz = self.Uz + UTemp


                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j*sig)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i)

                    self.Us = self.Us + UTemp

                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i)

                    self.Up = self.Up + UTemp


            self.Us = self.Us * sin(m*self.grid.phi3D)
            self.Uz = -self.Uz * sin(m*self.grid.phi3D)
            self.Up = self.Up * cos(m*self.grid.phi3D)


        if (symm == 'ea') or (symm == 'EA'):
        
            
            for i in range(N+1):
                for j in range(N-i+1):
                    
            
                    C = (-1)**(i+j) * dfactorial(2*(m+N+i+j)+1)/  \
                        ( 2**(j+1) * dfactorial(2*i+1) * factorial(N-i-j)  \
                        * factorial(i) * factorial(j) * factorial(m+j) )

                    UTemp = C * sig**(2*i-1) * ( 1 - sig**2)**j * (2*i+1) * \
                            self.grid.s3D**(m+2*j) * self.grid.z3D**(2*j)

                    self.Uz = self.Uz + UTemp


                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j*sig)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i+1)

                    self.Us = self.Us + UTemp


                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i+1)


                    self.Up = self.Up + UTemp


            self.Us = self.Us * sin(m*self.grid.phi3D)
            self.Uz = -self.Uz * sin(m*self.grid.phi3D)
            self.Up = self.Up * cos(m*self.grid.phi3D)

            del UTemp
