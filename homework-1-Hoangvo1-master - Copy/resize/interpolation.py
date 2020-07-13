class interpolation():
   
    def linear_interpolation(self, pt1, pt2, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        #Write your code for linear interpolation here
        if pt1[0]==pt2[0]:
            intensity = pt1[2]
        else:
            I1 = pt1[2]
            I2 = pt2[2]
            find1 = float(I1*(pt2[0]-unknown[0])/(pt2[0]-pt1[0]))
            find2 = float(I2*(unknown[0]-pt1[0])/(pt2[0]-pt1[0]))
            intensity = int(round(find1+find2))

        return intensity

    def bilinear_interpolation(self, pt1, pt2, pt3, pt4, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        pt1: known point pt3 and f(pt3) or intensity value
        pt2: known point pt4 and f(pt4) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        # Write your code for bilinear interpolation here
        # May be you can reuse or call linear interpolatio method to compute this task
        f1 = self.linear_interpolation(pt1, pt3, unknown)
        f2 = self.linear_interpolation(pt2, pt4, unknown)
        y1 = pt1[1]
        y2 = pt2[1]
        y = unknown[1]
        if y1==y2:
            intensity = f1
        else:
            find1= float(f1*(y2-y)/(y2-y1))
            find2= float(f2*(y-y1)/(y2-y1))
            intensity = int(round(find1 + find2))
                
        return intensity

