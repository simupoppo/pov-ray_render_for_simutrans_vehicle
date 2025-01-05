import subprocess as sb
import os
import datetime

class render_povray():
    def __init__(self,infile,outfile,paksize,tilesize_x=1,tilesize_y=1,tilesize_z=1,winter=0,make_front=0,pakstr="pak128japan"):
        self.infile=infile
        self.outfile=outfile
        self.paksize=int(paksize)
        self.Nx=int(tilesize_x)
        self.Ny=int(tilesize_y)
        self.Nz=int(tilesize_z)
        self.winter=int(winter)
        self.make_front=int(make_front)
        self.pakstr=pakstr
    def flag(self):
        def declare_povray(param,input_str):
            return "#declare "+str(param)+"="+str(input_str)+";\n"
        if self.paksize%4==0:
            # filesize define
            Width=self.paksize*(max(self.Nx,self.Ny))*8
            Height=self.paksize*(max(self.Nx,self.Ny,self.Nz//2))
            # make inc file which defines some values. 
            temp_inc_filepath=os.path.dirname(self.infile)+"/temp.inc"
            with open(temp_inc_filepath,mode="w") as f:
                f.write(declare_povray("int_x",self.Nx))
                f.write(declare_povray("int_y",self.Ny))
                f.write(declare_povray("int_z",max(self.Nz,1)))
                f.write(declare_povray("number_width",max(self.Nx,self.Ny)))
                f.write(declare_povray("number_hight",max(self.Nx,self.Ny,self.Nz//2)))
                f.write(declare_povray("winter",self.winter))
                f.write(declare_povray("make_front_image",self.make_front))
                f.write(declare_povray("pak_str",'"'+self.pakstr+'"'))
            # rendering
            outname=self.outfile[:-4]
            if outname=="":
                outname=self.infile[:-4]
            if self.winter==1:
                outname+="-winter"
            try:
                sb.run(["pvengine.exe","/NR","/EXIT","/RENDER",str(self.infile),"Width="+str(Width),"Height="+str(Height),"Antialias=Off","+O"+outname])
            except:
                try:
                    sb.run(["povray",str(self.infile),"Width="+str(Width),"Height="+str(Height),"Antialias=Off","+O"+outname])
                except:
                    return False
            if os.path.isfile(outname+".png")==False:
                return False
            elif os.path.isfile(outname+"_0.png"):
                t_1=os.path.getmtime(outname+".png")
                t_2=os.path.getmtime(outname+"_0.png")
                if (t_1<t_2):
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

class povray_template():
    def __init__(self,outfile):
        self.outfile=outfile
    def write_snow(self,out):
        snow_outfile=os.path.dirname(out)+"/snow.inc"
        with open(snow_outfile,mode="w") as f:
            f.write("#declare winter_light=\n")
            f.write("light_source {\n\t<0,173,0>\n\tcolor rgb 33\n\tparallel\n\tpoint_at<0,0,0>\n}\n")
        return
    def write_file(self,out):
        with open(out,mode="w") as f:
            f.write('#include "snow.inc"\n#include "temp.inc"\n')
            f.write('// ---add include files---\n\n\n')
            f.write('// -----------------------\n')
            f.write('// The default tile scale in this pov-ray file (not for pak file)\n')
            f.write('#local paksize=64;\n\n\n')
            f.write('// ---camera setting---\n')
            f.write('camera {\n\torthographic\n\tlocation <100,81.64965809277,100>*number_hight*paksize/128\n\tlook_at <0,0.5,0>*paksize/128\n\tright<1,0,-1> *paksize*number_width*4\n\tup<1,0,1>  *paksize*number_hight/2\n\t}\n\n\n')
            f.write('// ---light setting---\n')
            f.write('light_source {\n\t<0,173,100>\n\tcolor rgb 1\n\tparallel\n\tpoint_at<0,0,0>\n}\n// If winter==1, set a light to make the snow cover.\n#if(winter)\n\tlight_source{winter_light}\n#end\n\n\n')
            f.write('// ----------------------------------\n')
            f.write('//\n')
            f.write('// the name of the object with all objects merged must be "obj"\n')
            f.write('//\n')
            f.write('// ---make objects below this line---\n')
            f.write('#declare obj=\n')
            f.write('\n\n\n\n\n\n\n\n\n\n\n\n')
            f.write('// ---make objects above this line---\n')
            f.write('// \n//\n//\n')
            f.write('// ---set the offset---\n')
            f.write('#switch(0)\n')
            f.write('\t#case (strcmp(pak_str,"pak128japan"))\n')
            f.write('\t\t#debug "pak128.japan"\n')
            f.write('\t\t#declare offset_S = <-1,0,-14>;\n')
            f.write('\t\t#declare offset_E = <-14,0,-1>;\n')
            f.write('\t\t#declare offset_SE = <-1,0,-1>*11;\n')
            f.write('\t\t#declare offset_SW = <1,0,-1>*22.75/4;\n')
            f.write('\t\t#declare offset_N = <-1,0,11>;\n')
            f.write('\t\t#declare offset_W = <11,0,-1>;\n')
            f.write('\t\t#declare offset_NW = <1,0,1>*13;\n')
            f.write('\t\t#declare offset_NE = <-1,0,1>*22.75/4;\n')
            f.write('\t#break\n')
            f.write('\t#else\n')
            f.write('\t\t#debug "this paksize offset is undefined!"\n')
            f.write('\t\t#declare offset_S = <0,0,-1>*0;\n')
            f.write('\t\t#declare offset_E = <-1,0,0>*0;\n')
            f.write('\t\t#declare offset_SE = <-1,0,-1>*0;\n')
            f.write('\t\t#declare offset_SW = <1,0,-1>*0;\n')
            f.write('\t\t#declare offset_N = <0,0,1>*0;\n')
            f.write('\t\t#declare offset_W = <1,0,0>*0;\n')
            f.write('\t\t#declare offset_NW = <1,0,1>*0;\n')
            f.write('\t\t#declare offset_NE = <-1,0,1>*0;\n')
            f.write('#end\n')
            f.write('// ---put the obj---\n')
            f.write('#declare output_obj=\nobject{\n\tobj\n}\n')
            f.write('#declare output_obj_S=\nobject{\n\toutput_obj\n\ttranslate offset_S\n}\n')
            f.write('#declare output_obj_E=\nobject{\n\toutput_obj\n\ttranslate<-1,0,-1>*paksize*int_x/4\n\trotate<0,90,0>\n\ttranslate<1,0,1>*paksize*int_x/4\n\ttranslate offset_E\n}\n')
            f.write('#declare output_obj_SE=\nobject{\n\toutput_obj\n\ttranslate<-1,0,-1>*paksize*int_x/4\n\trotate<0,45,0>\n\ttranslate<1,0,1>*paksize*int_x/4\n\ttranslate offset_SE\n}\n')
            f.write('#declare output_obj_SW=\nobject{\n\toutput_obj\n\ttranslate<-1,0,-1>*paksize*int_x/4\n\trotate<0,-45,0>\n\ttranslate<1,0,1>*paksize*int_x/4\n\ttranslate offset_SW\n}\n')
            f.write('#declare output_obj_N=\nobject{\n\toutput_obj\n\ttranslate<-1,0,-1>*paksize*int_x/4\n\trotate<0,180,0>\n\ttranslate<1,0,1>*paksize*int_x/4\n\ttranslate offset_N\n}\n')
            f.write('#declare output_obj_W=\nobject{\n\toutput_obj\n\ttranslate<-1,0,-1>*paksize*int_x/4\n\trotate<0,270,0>\n\ttranslate<1,0,1>*paksize*int_x/4\n\ttranslate offset_W\n}\n')
            f.write('#declare output_obj_NW=\nobject{\n\toutput_obj\n\ttranslate<-1,0,-1>*paksize*int_x/4\n\trotate<0,-135,0>\n\ttranslate<1,0,1>*paksize*int_x/4\n\ttranslate offset_NW\n}\n')
            f.write('#declare output_obj_NE=\nobject{\n\toutput_obj\n\ttranslate<-1,0,-1>*paksize*int_x/4\n\trotate<0,135,0>\n\ttranslate<1,0,1>*paksize*int_x/4\n\ttranslate offset_NE\n}\n')
            f.write('// Place objects in 8 directions\n')
            f.write('object{merge{\n\t')
            f.write('object{\n\toutput_obj_S\n\t\ttranslate<-1,0,1>*paksize*number_width*7/4\n\t}\n\t')
            f.write('object{\n\toutput_obj_E\n\t\ttranslate<-1,0,1>*paksize*number_width*5/4\n\t}\n\t')
            f.write('object{\n\toutput_obj_SE\n\t\ttranslate<-1,0,1>*paksize*number_width*3/4\n\t}\n\t')
            f.write('object{\n\toutput_obj_SW\n\t\ttranslate<-1,0,1>*paksize*number_width*1/4\n\t}\n\t')
            f.write('object{\n\toutput_obj_N\n\t\ttranslate<-1,0,1>*paksize*number_width*(-1)/4\n\t}\n\t')
            f.write('object{\n\toutput_obj_W\n\t\ttranslate<-1,0,1>*paksize*number_width*(-3)/4\n\t}\n\t')
            f.write('object{\n\toutput_obj_NW\n\t\ttranslate<-1,0,1>*paksize*number_width*(-5)/4\n\t}\n\t')
            f.write('object{\n\toutput_obj_NE\n\t\ttranslate<-1,0,1>*paksize*number_width*(-7)/4\n\t}\n\t')
            f.write('}\n\tscale<1,.8165,1> // To set 1 distance of y direction as 1px, rescaling the hight\n}\n')
        return
    def make_template(self):
        self.write_snow(self.outfile)
        print("make snow.inc")
        self.write_file(self.outfile)
        print("make "+self.outfile)
        print("make templates successfully")
        return