import bpy
from math import degrees,radians
from mathutils import Euler
from os import system
import requests

URL = "uri"

class SimpleBoneAnglesPanel(bpy.types.Panel):
    bl_label = "Bone Angles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):

        row = self.layout.row()
        values = AngleHelper.segment_rotation()
        row.label(text='Angle A: {:.2f}'.format(values[0]))
        row.operator("berthelette.senda")
        row = self.layout.row()
        row.label(text='Angle B: {:.2f}'.format(values[1]))
        row.operator("berthelette.sendb")
        row = self.layout.row()
        row.label(text='Angle C: {:.2f}'.format(values[2]))
        row.operator("berthelette.sendc")
        row = self.layout.row()
        row.label(text='Angle D: {:.2f}'.format(values[3]))
        row.operator("berthelette.sendd")
        row = self.layout.row()
        row.label(text='Servo A: {:.2f}'.format(values[4]))   
        row.operator("berthelette.servoa")     
        row = self.layout.row()
        row.operator("berthelette.sendall")
        row = self.layout.row()
        row.operator("berthelette.init")
        row = self.layout.row()
        row.prop(bpy.context.scene,'ServoB')
        row.operator("berthelette.servob")
        row = self.layout.row()
        row.prop(bpy.context.scene,'ServoC')
        row.operator("berthelette.servoc")
 
class AngleHelper():

    def restraint_angle(angle):
        if angle > 180:
            return -360+angle  
        elif angle < -180:
            return angle + 360
        else:
            return angle
     
    def get_rotation(bone):
        mat = bone.matrix.to_euler()
        return(round(degrees(mat.x),2), round(degrees(mat.y),2), round(degrees(mat.z),2))
        
    def segment_rotation():        
        arm = bpy.context.scene.objects['Armature']
        bone_0= arm.pose.bones['Bone']
        bone_1 = arm.pose.bones['Bone.001']
        bone_2 = arm.pose.bones['Bone.002']
        bone_3 = arm.pose.bones['Bone.003']
        angle_D = AngleHelper.get_rotation(bone_0)[2]
        angle_A = AngleHelper.get_rotation(bone_0)[1] if AngleHelper.get_rotation(bone_0)[0] >0 else 180-AngleHelper.get_rotation(bone_0)[1] 
        angle_B = -angle_A+ (AngleHelper.get_rotation(bone_1)[1]if AngleHelper.get_rotation(bone_1)[0] >0 else 180-AngleHelper.get_rotation(bone_1)[1])    
        angle_C = -angle_A-angle_B+(AngleHelper.get_rotation(bone_2)[1]if AngleHelper.get_rotation(bone_2)[0] >0 else 180-AngleHelper.get_rotation(bone_2)[1])
        angle_servo_A = degrees(bone_3.rotation_axis_angle[0])
        return(AngleHelper.restraint_angle(angle_A), AngleHelper.restraint_angle(angle_B),AngleHelper.restraint_angle(angle_C),AngleHelper.restraint_angle(angle_D), angle_servo_A)
    
class InitRequest(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.init"
    bl_label = "Initialize Pose"
    bl_description = 'Initialize Berthelette Pose'
    
    def execute(self, context):   
        response = requests.get('http://192.168.1.32:5000/init')
              
        return{'FINISHED'}  
    
class SendA(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.senda"
    bl_label = "Send A"
    bl_description = 'Send angle A'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://192.168.1.32:5000/angleA/{:.2f}'.format(values[0]))
              
        return{'FINISHED'}  

class SendB(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.sendb"
    bl_label = "Send B"
    bl_description = 'Send angle B'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URL+':5000/angleB/{:.2f}'.format(values[1]))
              
        return{'FINISHED'}  
        
class SendC(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.sendc"
    bl_label = "Send C"
    bl_description = 'Send angle C'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URL+':5000/angleC/{:.2f}'.format(values[2]))
              
        return{'FINISHED'}  
        
class SendD(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.sendd"
    bl_label = "Send D"
    bl_description = 'Send angle D'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URL+':5000/angleD/{:.2f}'.format(values[3]))
              
        return{'FINISHED'}  

class SendAll(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.sendall"
    bl_label = "Send All"
    bl_description = 'Send all angles'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URL+':5000/angleAll/{:.2f}/{:.2f}/{:.2f}/{:.2f}'.format(values[0],values[1],values[2],values[3]))
              
        return{'FINISHED'}  
    
class ServoA(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.servoa"
    bl_label = "Send ServoA"
    bl_description = 'Send angle of servoA'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URL+':5000/servoA/{:.2f}'.format(values[4]))
              
        return{'FINISHED'}  
                
    
class ServoB(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.servob"
    bl_label = "Send ServoB"
    bl_description = 'Send angle of servoB'
    
    def execute(self, context):   
        response = requests.get('http://'+URL+':5000/servoB/{:.2f}'.format(bpy.context.scene.ServoB))
              
        return{'FINISHED'}  
                
    
class ServoC(bpy.types.Operator): #fait un rendu de toutes les scenes
    bl_idname = "berthelette.servoc"
    bl_label = "Send ServoC"
    bl_description = 'Send angle of servoC'
    
    def execute(self, context):   
        response = requests.get('http://'+URL+':5000/servoC/{:.2f}'.format(bpy.context.scene.ServoC))
              
        return{'FINISHED'}  
                

bpy.types.Scene.ServoB = bpy.props.FloatProperty(default=90, min=0, max=180, step=500)
bpy.types.Scene.ServoC = bpy.props.FloatProperty(default=90, min=0, max=180, step=500)
bpy.utils.register_class(InitRequest)
bpy.utils.register_class(ServoA)
bpy.utils.register_class(ServoB)
bpy.utils.register_class(ServoC)
bpy.utils.register_class(SendA)
bpy.utils.register_class(SendB)
bpy.utils.register_class(SendC)
bpy.utils.register_class(SendD)
bpy.utils.register_class(SendAll)
bpy.utils.register_class(SimpleBoneAnglesPanel)