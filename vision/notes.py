'''
Assignments:


Edge detection:
    Color differential
    Pixel values differnt
    
    a.k.a. Intensity difference peaks
    
    gradient, Gx = (-1 0 1)
                   (-2 0 2)
                   (-1 0 1)
                   
              Gy = ( 1  2  1)
                   ( 0  0  0)
                   (-1 -2 -1)
                     
            this is the derivative in the x or y direction
    
            Gx^2 + Gy^2 > T
            
            
Improving Sobel:
    thin the edges,
    refine the edges
        remove noise, connect certain edges


    Canny Edge detection:
        Consider potential edge pixel p to nearest neighbors along the perpendicular to the supposed edge
        Only keep p as an edge if its G value is the maximum
        
    ø = atan2(Gy, Gx)

    Get rid of isolated artifacts:
        

'''

