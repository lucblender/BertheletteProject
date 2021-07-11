import bpy
from math import degrees,radians
from mathutils import Euler
from os import system
import requests
import threading
from time import sleep

URI = "192.168.1.32"

head_selection = [('Finger','4 Fingers Claw','4 Fingers Claw'),
                    ('TPU','TPU Claw','TPU Claw'),
                    ('Vaccum','Vaccum Head','Vaccum Head')]
                    
pump_status = [('On','Pump On','4 Fingers Claw'),
                    ('Off','Pump Off','TPU Claw')]
                    
                    
class SimpleBoneAnglesPanel(bpy.types.Panel):
    bl_category  = "Berthelette"
    bl_label = "Bone Angles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):

        #row = self.layout.row()
        box = self.layout.box()  
        row=box.row() 
        row.label(text="Angles parameters")
        row=box.row() 
        row.operator("berthelette.init", icon="FILE_REFRESH")
        
        inner_box = box.box()  
        row=inner_box.row()         
        row.label(text="Init single motor")
        row=inner_box.row()   
        row.operator("berthelette.inita", icon="FILE_REFRESH", text="A")
        row.operator("berthelette.initb", icon="FILE_REFRESH", text="B")
        row.operator("berthelette.initc", icon="FILE_REFRESH", text="C")
        row.operator("berthelette.initd", icon="FILE_REFRESH", text="D")
        row=box.row() 
        values = AngleHelper.segment_rotation()
        row.label(text='Angle A: {:.2f}'.format(values[0]))
        row.operator("berthelette.senda")
        row=box.row() 
        row.label(text='Angle B: {:.2f}'.format(values[1]))
        row.operator("berthelette.sendb")
        row=box.row() 
        row.label(text='Angle C: {:.2f}'.format(values[2]))
        row.operator("berthelette.sendc")
        row=box.row() 
        row.label(text='Angle D: {:.2f}'.format(values[3]))
        row.operator("berthelette.sendd")
        row=box.row() 
        row.operator("berthelette.sendall", icon="CONSTRAINT")
        
         
        box = self.layout.box()  
        row=box.row() 
        row.label(text="Head parameters")
        row=box.row()
        row.prop(bpy.context.scene,'ClawSelector')
        row=box.row()
        row.label(text='Servo A: {:.2f}'.format(values[4]))   
        row.operator("berthelette.servoa")        
        
        
        if context.scene.ClawSelector == {"Vaccum"}:
            row=box.row() 
            row.prop(bpy.context.scene,'PumpStatus')
        
        row=box.row()                  
        c1 = row.column()
        c2 = row.column()  
        c1.prop(bpy.context.scene,'ServoB')
        c2.operator("berthelette.servob")
        if context.scene.ClawSelector == {"Vaccum"}:
            c1.enabled = False
        else:
            c1.enabled = True
        row=box.row()             
        c1 = row.column()
        c2 = row.column()  
        c1.prop(bpy.context.scene,'ServoC')
        c2.operator("berthelette.servoc")
        if context.scene.ClawSelector == {"Vaccum"}:
            c1.enabled = False
        else:
            c1.enabled = True
        row=box.row()  
        box.operator('berthelette.servoall', icon="CONSTRAINT")
        
          
        box = self.layout.box()  
        row=box.row() 
        row.label(text="Solenoid clamp")   
        row=box.row() 
        row.operator("berthelette.sendsolenoid") 
        row=box.row()
        row.prop(bpy.context.scene,'SolenoidStatus', text="Open solenoid clamp")
        
        box = self.layout.box()  
        row=box.row() 
        row.label(text="Sequence parameters")
        row=box.row() 
        row.label(text="First frame")
        row.prop(bpy.context.scene,'StartSequence', text="")
        row=box.row() 
        row.label(text="Last frame")
        row.prop(bpy.context.scene,'StopSequence', text="")
        row=box.row()
        row.label(text="Delay between frame [s]")
        row.prop(bpy.context.scene,'DelaySequence', text="")        
        row=box.row() 
        row.operator("berthelette.sendsequence", icon="PLAY")
       
 
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
        angle_servo_A_tmp = degrees(bone_3.rotation_euler[1])
        if angle_servo_A_tmp<-90:
            angle_servo_A_tmp = -90
        elif angle_servo_A_tmp > 90:
            angle_servo_A_tmp = 90
        

        angle_servo_A = 180 - (angle_servo_A_tmp + 90)
        return(AngleHelper.restraint_angle(angle_A), AngleHelper.restraint_angle(angle_B),AngleHelper.restraint_angle(angle_C),AngleHelper.restraint_angle(angle_D), angle_servo_A)
    
class InitRequest(bpy.types.Operator):
    bl_idname = "berthelette.init"
    bl_label = "Initialize Pose"
    bl_description = 'Initialize Berthelette Pose'
    
    def execute(self, context):   
        response = requests.get('http://'+URI+':5000/init')
              
        return{'FINISHED'}  
        
class InitARequest(bpy.types.Operator):
    bl_idname = "berthelette.inita"
    bl_label = "Initialize A Pose"
    bl_description = 'Initialize A Berthelette Pose'
    
    def execute(self, context):   
        response = requests.get('http://'+URI+':5000/initA')
              
        return{'FINISHED'}    
          
class InitBRequest(bpy.types.Operator):
    bl_idname = "berthelette.initb"
    bl_label = "Initialize B Pose"
    bl_description = 'Initialize B Berthelette Pose'
    
    def execute(self, context):   
        response = requests.get('http://'+URI+':5000/initB')
              
        return{'FINISHED'} 
             
class InitCRequest(bpy.types.Operator):
    bl_idname = "berthelette.initc"
    bl_label = "Initialize C Pose"
    bl_description = 'Initialize C Berthelette Pose'
    
    def execute(self, context):   
        response = requests.get('http://'+URI+':5000/initC')
              
        return{'FINISHED'}   
           
class InitDRequest(bpy.types.Operator):
    bl_idname = "berthelette.initd"
    bl_label = "Initialize D Pose"
    bl_description = 'Initialize D Berthelette Pose'
    
    def execute(self, context):   
        response = requests.get('http://'+URI+':5000/initD')
              
        return{'FINISHED'}  
    
class SendA(bpy.types.Operator):
    bl_idname = "berthelette.senda"
    bl_label = "Send A"
    bl_description = 'Send angle A'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URI+':5000/angleA/{:.2f}'.format(values[0]))
              
        return{'FINISHED'}  

class SendB(bpy.types.Operator):
    bl_idname = "berthelette.sendb"
    bl_label = "Send B"
    bl_description = 'Send angle B'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URI+':5000/angleB/{:.2f}'.format(values[1]))
              
        return{'FINISHED'}  
        
class SendC(bpy.types.Operator):
    bl_idname = "berthelette.sendc"
    bl_label = "Send C"
    bl_description = 'Send angle C'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URI+':5000/angleC/{:.2f}'.format(values[2]))
              
        return{'FINISHED'}  
        
class SendD(bpy.types.Operator):
    bl_idname = "berthelette.sendd"
    bl_label = "Send D"
    bl_description = 'Send angle D'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URI+':5000/angleD/{:.2f}'.format(values[3]))
              
        return{'FINISHED'}  

class SendAll(bpy.types.Operator):
    bl_idname = "berthelette.sendall"
    bl_label = "Send All"
    bl_description = 'Send all angles'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URI+':5000/angleAll/{:.2f}/{:.2f}/{:.2f}/{:.2f}'.format(values[0],values[1],values[2],values[3]))
              
        return{'FINISHED'}  
    
class SendSolenoid(bpy.types.Operator):
    bl_idname = "berthelette.sendsolenoid"
    bl_label = "Send Solenoid"
    bl_description = 'Send solenoid, autoclose after 5 secs'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        if context.scene.SolenoidStatus == True:
            response = requests.get('http://'+URI+':5000/openSolenoid')
            print("open")
        else:
            response = requests.get('http://'+URI+':5000/closeSolenoid')
            print("close")
              
        return{'FINISHED'}  
    
class SendSequence(bpy.types.Operator):
    bl_idname = "berthelette.sendsequence"
    bl_label = "Send Sequence"
    bl_description = 'Send all angles in sequence'

    _timer = None
    t = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # change theme color, silly!        
            if self.t.isAlive() == False:
                if bpy.context.scene.frame_current == bpy.context.scene.StopSequence:
                    self.cancel(context)
                    return {'CANCELLED'}
                else:
                    bpy.context.scene.frame_set(bpy.context.scene.frame_current+1)
                    self.t = threading.Thread(target=self.requestLongPoll, args=())
                    self.t.start()

        return {'PASS_THROUGH'}

    def requestLongPoll(self):
        values = AngleHelper.segment_rotation()
        
        bpy.ops.berthelette.sendsolenoid()
        
        response = requests.get('http://'+URI+':5000/angleAllLonpoll/{:.2f}/{:.2f}/{:.2f}/{:.2f}/{:.2f}/{:.2f}/{:.2f}'.format(values[0],values[1],values[2],values[3],values[4],bpy.context.scene.ServoB,bpy.context.scene.ServoC))
        sleep(bpy.context.scene.DelaySequence)

    def execute(self, context):
        bpy.context.scene.frame_set(bpy.context.scene.StartSequence)
        wm = context.window_manager
        self._timer = wm.event_timer_add(.5, window=context.window)
        wm.modal_handler_add(self)
        self.t = threading.Thread(target=self.requestLongPoll, args=())
        self.t.start()
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    
class ServoA(bpy.types.Operator):
    bl_idname = "berthelette.servoa"
    bl_label = "Send ServoA"
    bl_description = 'Send angle of servoA'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URI+':5000/servoA/{:.2f}'.format(values[4]))
              
        return{'FINISHED'}  
                
    
class ServoB(bpy.types.Operator):
    bl_idname = "berthelette.servob"
    bl_label = "Send ServoB"
    bl_description = 'Send angle of servoB'
    
    def execute(self, context):   
        response = requests.get('http://'+URI+':5000/servoB/{:.2f}'.format(bpy.context.scene.ServoB))
              
        return{'FINISHED'}  
                
    
class ServoC(bpy.types.Operator):
    bl_idname = "berthelette.servoc"
    bl_label = "Send ServoC"
    bl_description = 'Send angle of servoC'
    
    def execute(self, context):   
        response = requests.get('http://'+URI+':5000/servoC/{:.2f}'.format(bpy.context.scene.ServoC))
              
        return{'FINISHED'}  
   
class ServoAll(bpy.types.Operator):
    bl_idname = "berthelette.servoall"
    bl_label = "Send all servos"
    bl_description = 'Send angle all Servo'
    
    def execute(self, context):   
        values = AngleHelper.segment_rotation()
        response = requests.get('http://'+URI+':5000/servoAll/{:.2f}/{:.2f}/{:.2f}'.format(values[4],bpy.context.scene.ServoB,bpy.context.scene.ServoC))
              
        return{'FINISHED'}  
                    
def servoB_set(self, value):
    if self.ClawSelector == {'TPU'}:
        if value > 50:
            value = 50    
    
    self["ServoB"] = value
    
old_value = None                
def servoB_get(self):
    global old_value
    value = self["ServoB"]
    if old_value != value:
        if self.ClawSelector == {'TPU'}:
            bpy.data.objects['Gear left'].rotation_euler[1] = radians(-value)
            bpy.data.objects['Gear right'].rotation_euler[1] = radians(value)
        elif self.ClawSelector == {"Finger"}:
            bpy.data.objects['Finger_1'].rotation_euler[1] = radians(-90+value/7.2)
            bpy.data.objects['Finger_2'].rotation_euler[1] = radians(-90-value/7.2)
            bpy.data.objects['Finger_3'].rotation_euler[1] = radians(-90-value/7.2)
            bpy.data.objects['Finger_4'].rotation_euler[1] = radians(-90-value/7.2)
        elif self.ClawSelector == {"Vaccum"}:
            pass
    old_value = value
    return self.get("ServoB", 0.0)

def clawSelector_update(self, context):
    if self.ClawSelector == {"TPU"}:
        bpy.data.collections['Fingers Claw'].hide_viewport = True
        bpy.data.collections['TPU Claw'].hide_viewport = False
        bpy.data.collections['Vaccum Head'].hide_viewport = True
    elif self.ClawSelector == {"Finger"}:
        bpy.data.collections['Fingers Claw'].hide_viewport = False
        bpy.data.collections['TPU Claw'].hide_viewport = True
        bpy.data.collections['Vaccum Head'].hide_viewport = True
    elif self.ClawSelector == {"Vaccum"}:
        bpy.data.collections['Fingers Claw'].hide_viewport = True
        bpy.data.collections['TPU Claw'].hide_viewport = True
        bpy.data.collections['Vaccum Head'].hide_viewport = False
        
def pumpStatus_update(self, context):
    if self.PumpStatus == {"On"}:
        context.scene.ServoB = 0
        context.scene.ServoC = 180
    elif self.PumpStatus == {"Off"}:
        context.scene.ServoB = 180
        context.scene.ServoC = 0

     
class_list = (InitARequest,
    InitBRequest,
    InitCRequest,
    InitDRequest,
    InitRequest,
    ServoA,
    ServoB,
    ServoC,
    ServoAll,
    SendA,
    SendB,
    SendC,
    SendD,
    SendAll,
    SendSequence,
    SimpleBoneAnglesPanel,
    SendSolenoid
    )           
def register(): 
    bpy.types.Scene.ServoB = bpy.props.FloatProperty(default=90, min=0, max=180, step=500, set=servoB_set, get=servoB_get)
    bpy.types.Scene.ServoC = bpy.props.FloatProperty(default=90, min=0, max=180, step=500)

    bpy.types.Scene.StartSequence = bpy.props.IntProperty(default=0, min=0, step=1)
    bpy.types.Scene.StopSequence = bpy.props.IntProperty(default=0, min=0, step=1)
    bpy.types.Scene.DelaySequence = bpy.props.FloatProperty(default=0, min=0, step=50)
    
    bpy.types.Scene.SolenoidStatus = bpy.props.BoolProperty(default=False)

    bpy.types.Scene.ClawSelector = bpy.props.EnumProperty(items=head_selection,options={'ENUM_FLAG'}, default = {"Finger"}, update=clawSelector_update)
    bpy.types.Scene.PumpStatus = bpy.props.EnumProperty(items=pump_status,options={'ENUM_FLAG'}, default = {"Off"}, update=pumpStatus_update)
    
    for cls in class_list:
        bpy.utils.register_class(cls)
    
def unregister():    
    for cls in class_list:
        bpy.utils.unregister_class(cls)

 
if __name__ == "__main__": #
    register()
