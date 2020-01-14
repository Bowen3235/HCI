import tkinter as tk
import time
from PIL import Image, ImageTk, ImageFilter
from pyscreeze import screenshot as grab
#from pycreenshot import grab
import numpy as np
from os import listdir, path

shotratio = 2

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb  

State = {
	'Init':0 ,
	'changing':1, }
Height = int(736/1)
Width  = int(414/1)

First_Use = True
DEBUG = False
#140,250,40,40
# #FAF8E1
class window( object ):
	def __init__(self):

		self.root = tk.Tk()
		self.root.title( 'Simulation' )
		self.root.geometry( str(Width)+'x'+str(Height)+'+0+0' )
		self.root.resizable(0, 0)
		#self.root.wm_attributes("-transparent", True)

		self.container = tk.Frame( self.root )
		self.container.pack(side="top", fill="both", expand=True)
		self.state = 'init'
		self.temp = tk.Frame( self.root )


		

		self.init_new_app( self, self.root , self.state )
		self.init_bind_app( )
		self.app = app( self, self.root , self.state )
		self.outside = outside( self, self.root )
		self.root.mainloop()
	def call_new_app( self, number, tar ):
		if DEBUG:
			self.new_app.show( ['google'] )
		password = ""
		for i in range(len( number )):
			#print( number[i].get() )
			password +=  number[i].get() 
		print( 'target: ',tar )
		print( 'input : ',password )
		if password == str(tar):
			self.new_app.show( ['google'] )
		else:
			size = { 'W':int(150/414*Width),'H':int(36/736*Height) }
			name = 'resource/error_number.png'
			self.app.show_error( name,size )
			
	def init_bind_app( self ):


		## choosing personal photo
		self.new_app.widgets['choosing_photo']['photo'].bind( 
			'<Button-1>',
			lambda event, var = ['photo_config','photo_config_list']:self.new_app.show( tar_show=var ) )
		
		##choosing photo config
		self.new_app.widgets['photo_config']['back'].bind(
			'<Button-1>',
			lambda event, var = ['choosing_photo']:self.new_app.show( var ))

		choosing_frame = lambda focus : \
		(\
			self.new_app.setting_var( type='aux' ,tar_frame='photo_config_list', name='now_focus' ,var = int( focus[focus.find('list')+4:] ) ),\
			\
			self.new_app.move_phote_on_canvas( tar_frame='photo_config_list',
				wid_name='list_canvas',
				tag = 'choosing_frame',
				position = { 'x':self.new_app.widgets['photo_config_list']['list_canvas'].coords( focus )[0], 
						'y':self.new_app.widgets['photo_config_list']['list_canvas'].coords( focus )[1] } ),\
			\
			self.new_app.widgets['photo_config_list']['list_canvas'].lift( 'choosing_frame' ),\
			self.new_app.change_photo( tar_frame='photo_config',
			wid_name='sure',
			new_path = 'resource/photo_config_sure_ready.png' )
		)

		for i in range( self.new_app.aux['photo_config_list']['number']+1 ):
			name = 'config_list'+str( i )
			self.new_app.widgets['photo_config_list'][ 'list_canvas' ].tag_bind(
				name,
				'<Button-1>',
				lambda event ,var = name : choosing_frame( var ) )
			#print( name )
			#print( type(
			#	self.new_app.widgets['photo_config_list']['list_canvas'].find_withtag( name )[0] ) ) 
		_ , size = self.new_app.making_ralative_pairs( 0, 0, 207, 159 )	
		if self.new_app.aux['photo_config_list']['number'] > 8 :
			layers = int( (self.new_app.aux['photo_config_list']['number']-1)/2)+1
			limit_height = ( layers - 4)*size['h']
			self.new_app.make_draggable(
			 	tar_frame = 'photo_config_list',
			 	wid_name = 'list_canvas',
			 	limit_height = limit_height
		)


		canvas_h = self.new_app.widgets['choosing_photo']['photo'].winfo_height()
		canvas_w = self.new_app.widgets['choosing_photo']['photo'].winfo_width()
		pic_h = size[ 'h' ]
		pic_w = size[ 'w' ]

		surefunc = lambda event :(\
			self.new_app.setting_var( type = 'aux' , tar_frame= 'choosing_photo' ,name= 'pic_path'  ,var = self.new_app.aux[ 'photo_config_list' ][ 'list_canvasconfig_list'+str( self.new_app.aux['photo_config_list']['now_focus'] )+'path' ] ),\
			self.new_app.widgets['choosing_photo']['photo'].itemconfig(
					'main', image = self.new_app.resource[ 'photo_config_list' ][ 'list_canvasconfig_list'+str( self.new_app.aux['photo_config_list']['now_focus'] )+'pic' ] ),\
			self.new_app.widgets['choosing_photo']['photo'].coords( 'main'
				,( int((canvas_w-pic_w)/2), int((canvas_h-pic_h)/2) ) ),\
			self.new_app.widgets['choosing_photo']['photo'].lift( 'frame' ),\
			self.new_app.show( ['choosing_photo'] )\
		)

		self.new_app.widgets[ 'photo_config' ][ 'sure' ].bind( '<Button-1>', surefunc )

		receive_user_info = lambda event, var=['tutorial_main_page'] : ( \
			self.new_app.show( var ),\
			self.new_app.setting_var( type = 'aux' , tar_frame= 'choosing_photo' ,name= 'user_name'  ,var= self.new_app.widgets['choosing_photo']['name_entry'].get() ) ,\
			self.new_app.move_phote_on_canvas( tar_frame='tutorial_main_page', wid_name='main_canvas',tag='tutorial_page_1' ),\
			print( 'user_name : ', self.new_app.aux['choosing_photo']['user_name'] ),\
			print( 'pic_path : ', self.new_app.aux['choosing_photo']['pic_path'] ),\
			self.new_app.setting_var( type = 'aux' , tar_frame= 'choosing_photo' ,name= 'late_time'  ,var=0 ),\
			np.savez('resource/user.npz',
				user_name = self.new_app.aux['choosing_photo']['user_name'],
				pic_path  = self.new_app.aux['choosing_photo']['pic_path'],
				time      = self.new_app.aux['choosing_photo']['late_time'],
				ratio	  = 0,
				friends   = 0,
				active    = 0,
				friends_list = []
				)\
			)
		self.new_app.widgets[ 'choosing_photo' ][ 'sure' ].bind( '<Button-1>', receive_user_info )

		for i in range( 1, 17 ):
			#print( 'tutorial_page_'+str( i ) )
			#print( 'tutorial_page_'+str( i+1 ) )
			self.new_app.widgets['tutorial_main_page']['main_canvas'].tag_bind(
				'tutorial_page_'+str( i ),
				'<Button-1>', 
				lambda event, i=i: 
					(\
					self.new_app.move_phote_on_canvas( tar_frame='tutorial_main_page', wid_name='main_canvas',tag='tutorial_page_'+str(i), position={'x':Width,'y':0} ),\
					self.new_app.move_phote_on_canvas( tar_frame='tutorial_main_page', wid_name='main_canvas',tag='tutorial_page_'+str(i+1), position={'x':0,'y':0} )\
					)
			)

		position, size = self.new_app.making_ralative_pairs( 247+55-71-28, 69+55-55-31, 143, 110 )
		self.new_app.widgets['tutorial_main_page']['main_canvas'].tag_bind(
				'tutorial_page_'+str( 17 ),
				'<Button-1>', 
				lambda event, i=['main_page']: 
					(\
						self.new_app.show( i ),\
						self.new_app.create_photo_on_canvas(
							tar_frame = 'main_page',
							wid_name = 'info_canvas',
							tag =  'personal_img',
							path = self.new_app.aux['choosing_photo']['pic_path'],
							size = size,
							position = position),\
						self.new_app.widgets['main_page']['info_canvas'].lift( 'main' ),\
						self.new_app.widgets['main_page']['info_canvas'].itemconfig(
							'name', text = self.new_app.aux[ 'choosing_photo' ][ 'user_name' ]
							),\
						self.new_app.widgets['main_page']['info_canvas'].lift('up'),\
						print( self.new_app.aux[ 'choosing_photo' ][ 'user_name' ] )\
					)
		)

		self.new_app.widgets[ 'main_page' ][ 'setting_canvas' ].tag_bind(
			'setting_setting',
			'<Button-1>',
			lambda event : self.new_app.show( ['setting_page'] )
		)

		self.new_app.widgets[ 'main_page' ][ 'setting_canvas' ].tag_bind(
			'setting_setting',
			'<Button-1>',
			lambda event : self.new_app.show( ['setting_page'] )
		)

		self.new_app.widgets['setting_page']['main_canvas'].tag_bind(
			'home_icon',
			'<Button-1>',
			lambda event : self.new_app.show( ['main_page'] )
		)

		self.new_app.widgets['setting_page']['main_canvas'].tag_bind(
			'personal_setting',
			'<Button-1>',
			lambda event : self.new_app.show( ['personal_page'] )
		)

		self.new_app.widgets['personal_page']['main_canvas'].tag_bind(
			'back',
			'<Button-1>',
			lambda event : self.new_app.show( ['setting_page'] )
		)

		self.new_app.widgets['setting_page']['main_canvas'].tag_bind(
			'about_setting',
			'<Button-1>',
			lambda event : self.new_app.show( ['about_page'] )
		)
		self.new_app.widgets['about_page']['main_canvas'].tag_bind(
			'back',
			'<Button-1>',
			lambda event : self.new_app.show( ['setting_page'] )
		)

		position_1, size = self.new_app.making_ralative_pairs( 30, 252-238, 296, 188 )
		func = lambda event, tar_frame = 'main_page', tag= 'gray', position={'x':Width, 'y':0} : (\
				self.new_app.move_phote_on_canvas( tar_frame, 'bg_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'info_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'setting_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'active_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'active_canvas' , 'messenge', position )\
		) 
		self.new_app.widgets['main_page']['bg_canvas'].tag_bind(
			'gray',
			'<Button-1>',
			func
		)
		self.new_app.widgets['main_page']['info_canvas'].tag_bind(
			'gray',
			'<Button-1>',
			func
		)
		self.new_app.widgets['main_page']['setting_canvas'].tag_bind(
			'gray',
			'<Button-1>',
			func
		)
		self.new_app.widgets['main_page']['active_canvas'].tag_bind(
			'gray',
			'<Button-1>',
			func
		)

		if self.new_app.aux['choosing_photo']['friends'] == 0:
			position_1, size = self.new_app.making_ralative_pairs( 30, 252-238, 296, 188 )
			func = lambda event, tar_frame = 'main_page', tag= 'gray', position={'x':-Width, 'y':-Height} : (\
				self.new_app.move_phote_on_canvas( tar_frame, 'bg_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'info_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'setting_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'active_canvas' , tag, position ),\
				self.new_app.move_phote_on_canvas( tar_frame, 'active_canvas' , 'messenge', position_1 )\
				) 
			self.new_app.widgets['main_page']['setting_canvas'].tag_bind(
				'add_setting',
				'<Button-1>',
				func
			)

		self.new_app.widgets['main_page']['setting_canvas'].tag_bind(
			'friends_setting',
			'<Button-1>',
			lambda event : self.new_app.show( ['adding_friend'] )
		)

		self.new_app.widgets['adding_friend']['header_canvas'].tag_bind(
			'home',
			'<Button-1>',
			lambda event : self.new_app.show( ['main_page'] )
		)

		self.new_app.widgets['adding_friend']['adding_canvas'].tag_bind(
			'ID_but',
			'<Button-1>',
			lambda event : self.new_app.show( ['ID_page'] )
		)

		self.new_app.widgets['ID_page']['main_canvas'].tag_bind(
			'back',
			'<Button-1>',
			lambda event : self.new_app.show( ['adding_friend'] )
		)






	def init_new_app( self, main_obj ,target, state ):
		## setting new app's content
		self.new_app = new_app( main_obj ,target, state )

		## google login
		self.new_app.add_frames( 'google' )
		position, size = self.new_app.making_pairs( 0,0,Width,Height )
		self.new_app.add_labels_with_image(
			'label', 
			'google',
			'bg',
			'resource/google_bg.png',
			size,
			position
		)
		self.new_app.add_frames( 'google_choose' )
		position, size = self.new_app.making_pairs( 0,0,Width,Height )
		self.new_app.add_labels_with_image(
			'label', 
			'google_choose',
			'bg',
			'resource/google_choose.png',
			size,
			position
		)

		self.new_app.add_frames( 'choosing_photo' )
		position, size = self.new_app.making_pairs( 0,0,Width,Height )
		self.new_app.add_labels_with_image(
			type = 'label', 
			tar_name ='choosing_photo',
			name = 'bg',
			path = 'resource/choosing_photo.png',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 180, 402, 200, 30 )
		self.new_app.add_labels_with_image(
			type = 'entry', 
			tar_name ='choosing_photo',
			name = 'name_entry',
			size = size,
			position = position
		)
		
		position, size = self.new_app.making_ralative_pairs( 123, 515, 66, 48 )
		self.new_app.add_labels_with_image(
			'label',
			'google',
			'no',
			'resource/no.png',
			size,
			position,
			func = lambda event, var = ['choosing_photo'], focus=self.new_app.widgets['choosing_photo']['name_entry'] : self.new_app.show( tar_show=var, setfocus=focus )
		)

		position, size = self.new_app.making_ralative_pairs( 234, 515, 66, 48 )
		self.new_app.add_labels_with_image(
			'label',
			'google',
			'yes',
			'resource/yes.png',
			size,
			position,
			func = lambda event, var = ['google_choose']: self.new_app.show( var )
		)

		position, size = self.new_app.making_ralative_pairs( 162, 511, 90, 50 )
		self.new_app.add_labels_with_image(
			'label',
			'google_choose',
			'cancel',
			'resource/cancell.png',
			size,
			position,
			func = lambda event, var =[ 'google' ]: self.new_app.show( var )
		)

		self.new_app.add_frames( 'google_password' )
		position, size = self.new_app.making_pairs( 0,0,Width,Height )
		self.new_app.add_labels_with_image(
			'label', 
			'google_password',
			'bg',
			'resource/google_password.png',
			size,
			position
		)

		position, size = self.new_app.making_ralative_pairs( 126, 386, 213, 34 )
		self.new_app.add_labels_with_image(
			type='entry',
			tar_name='google_password',
			name='password_entry',
			size=size,
			position=position,
			func = lambda event, var = ['google_password']: self.new_app.show( var ),
			show_mark = '*'
		)

		position, size = self.new_app.making_ralative_pairs( 112, 307, 202, 49 )
		self.new_app.add_labels_with_image(
			'label',
			'google_choose',
			'user1',
			'resource/user1.png',
			size,
			position,
			func = lambda event, var = ['google_password'], setforcus=self.new_app.widgets[ 'google_password' ]['password_entry']: self.new_app.show( tar_show=var, setfocus=setforcus )
		)

		

		## choosing personal photo


		## some about password
		position, size = self.new_app.making_ralative_pairs( 160, 509, 94, 48 )
		self.new_app.add_labels_with_image(
			type = 'label',
			tar_name = 'google_password',
			name = 'sure',
			path = 'resource/sure.png',
			size = size,
			position = position,
			func = lambda event, var = ['choosing_photo'], focus=self.new_app.widgets['choosing_photo']['name_entry'] : self.new_app.show( tar_show=var, setfocus=focus )
		)
		self.new_app.widgets[ 'google_password' ]['password_entry'].bind( '<Key>', 
			lambda event,tar_frame= 'google_password'
			,wid_name='sure'
			,new_path='resource/sure_ready.png'
			,condition=lambda var = self.new_app.widgets[ 'google_password' ]['password_entry'].get() : var != '' :self.new_app.change_photo( tar_frame, wid_name, new_path, condition )
		 )
		self.new_app.widgets[ 'google_password' ]['password_entry'].bind( '<BackSpace>', 
			lambda event,tar_frame= 'google_password'
			,wid_name='sure'
			,new_path='resource/sure.png'
			,condition=lambda var = self.new_app.widgets[ 'google_password' ]['password_entry'].get() : var == '' :self.new_app.change_photo( tar_frame, wid_name, new_path, condition )
		)
		## some about pass word
		'''
		position, size = self.new_app.making_ralative_pairs( 116, 186, 181, 181 )
		self.new_app.add_labels_with_image( 
			type = 'label',
			tar_name = 'choosing_photo',
			name = 'choosing_but',
			path = 'resource/Group 326.png',
			size = size,
			position = position,
			bg = '#FAF8E1'
		 )
		'''



		position, size = self.new_app.making_ralative_pairs( 128,196, 159, 159 )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'choosing_photo',
			name = 'photo',
			path = 'resource/Group 326.png',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 128,196, 159, 159 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'choosing_photo',
			wid_name = 'photo',
			tag = 'frame',
			path = 'resource/head_frame.png',
			size = size
		)

		self. new_app.aux[ 'choosing_photo' ][ 'pic_path' ] = 'resource/Group 326.png'



		position, size = self.new_app.making_pairs( 284, 468, 84, 29 )
		self.new_app.add_labels_with_image( 
			type = 'label',
			tar_name = 'choosing_photo',
			name = 'choosing_sure',
			path = 'resource/Group 325.png',
			size = size,
			position = position,
			bg = '#FAF8E1'
		 )

		## choosing photo_config

		self.new_app.add_frames( 'photo_config' )
		position, size = self.new_app.making_pairs( 0,0,Width,Height )
		self.new_app.add_labels_with_image(
			'label', 
			'photo_config',
			'bg',
			'resource/photo_config.png',
			size,
			position
		)

		position, size = self.new_app.making_ralative_pairs( 
			263, 34, 27, 15 )
		self.new_app.add_labels_with_image(
			type = 'label',
			tar_name = 'photo_config',
			name = 'back',
			path = 'resource/photo_config_back.png',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		##### photo_list

		self.new_app.add_frames( 'photo_config_list' )
		position, size = self.new_app.making_pairs( 0, 102, Width,Height )
		self.new_app.frames['photo_config_list'].place( x = position['x'], 
			y=position['y'], 
			width = size['w'],
			height = size['h'] )
		position, size = self.new_app.making_pairs( 0, 0, Width,Height )
		self.new_app.add_labels_with_image(
			type='canvas',
			tar_name='photo_config_list',
			name = 'list_canvas',
			size = size,
			position = position
		)
		position, size = self.new_app.making_ralative_pairs( 0, 0, 27, 15 )
		self.new_app.widgets[ 'photo_config_list' ][ 'list_canvas' ].place( x=position['x'], y=position['y'] )
		photos_list = listdir( 'resource/photo' )
		for i, name in enumerate( photos_list ):
			#print( 'config_list'+str(i) )
			position, size = self.new_app.making_ralative_pairs( int(i%2)*207, int(i/2)*159, 207, 159 )
			self.new_app.create_photo_on_canvas(
				tar_frame = 'photo_config_list',
				wid_name = 'list_canvas',
				tag = 'config_list'+str(i),
				path = 'resource/photo/'+name,
				size = size,
				position = position
			)
			self.new_app.widgets['photo_config_list']['list_canvas'].coords( 'config_list'+str(i),
				( position['x'], position['y'] ) )
		self.new_app.aux['photo_config_list']['number'] = i
		
		position, size = self.new_app.making_ralative_pairs( -207, 0, 207, 159 )	
		self.new_app.create_photo_on_canvas(
				tar_frame = 'photo_config_list',
				wid_name = 'list_canvas',
				tag = 'choosing_frame',
				path = 'resource/selected_frame.png',
				size = size,
				position = position
		)
		self.new_app.aux['photo_config_list']['now_focus'] = -1
		self.new_app.widgets[ 'photo_config_list' ][ 'list_canvas' ].config( height = size['h']*(int( (self.new_app.aux['photo_config_list']['number']-1)/2)+3 ) )
		self.new_app.widgets[ 'photo_config_list' ][ 'list_canvas' ].place( height = size['h']*(int( (self.new_app.aux['photo_config_list']['number']-1)/2)+3 ) )
		self.new_app.frames[ 'photo_config_list' ].place( height = size['h']*(int( (self.new_app.aux['photo_config_list']['number']-1)/2)+3 ) )

		position, size = self.new_app.making_ralative_pairs( 319, 26, 84, 29 )
		self.new_app.add_labels_with_image(
			type = 'label',
			tar_name = 'photo_config',
			name = 'sure',
			path = 'resource/photo_config_sure.png',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_ralative_pairs( 284, 468, 84, 29 )
		self.new_app.add_labels_with_image(
			type = 'label',
			tar_name = 'choosing_photo',
			name = 'sure',
			path = 'resource/photo_config_sure_ready.png',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		### main_page_tutorial

		position, size = self.new_app.making_ralative_pairs( 0, 0, Width, Height )
		self.new_app.add_frames( 'tutorial_main_page' )
		self.new_app.add_labels_with_image( 
			type='canvas',
			tar_name = 'tutorial_main_page',
			name = 'main_canvas',
			size = size,
			position = position
		)
		position, size = self.new_app.making_ralative_pairs( Width, 0, Width, Height )
		for i in range( 1, 18 ):
			#print( i )
			self.new_app.create_photo_on_canvas(
				tar_frame = 'tutorial_main_page',
				wid_name  = 'main_canvas',
				path  = 'resource/tutorial/tutorial'+str(i)+'.png',
				tag = 'tutorial_page_' + str(i) ,
				size = size,
				position = position
			)

		#### main page !!!! 

		## loading necessary information
		
		file = np.load( 'resource/user.npz' )
		file_1 = np.load( 'resource/friends.npz' )

		print( file['pic_path'] )
		if not First_Use:
			self.new_app.aux['choosing_photo']['late_time'] = file['time']
			self.new_app.aux['choosing_photo']['user_name'] = str(file['user_name'])
			self.new_app.aux['choosing_photo']['pic_path'] = str(file['pic_path'])
			self.new_app.aux['choosing_photo']['friends'] = int(file['friends'])
			self.new_app.aux['choosing_photo']['ratio'] = file['ratio']
			self.new_app.aux['choosing_photo']['active'] = int(file['active'])
			self.new_app.aux['choosing_photo']['friends_list'] = file['friends_list']
			self.new_app.aux['choosing_photo']['friends_info'] = file_1
		else:
			self.new_app.aux['choosing_photo']['late_time'] = 0
			self.new_app.aux['choosing_photo']['user_name'] = 'abc'
			self.new_app.aux['choosing_photo']['pic_path'] = 'resource/Group 326.png'
			self.new_app.aux['choosing_photo']['friends'] = 0
			self.new_app.aux['choosing_photo']['ratio'] = 0
			self.new_app.aux['choosing_photo']['active'] = 0
			self.new_app.aux['choosing_photo']['friends_list'] = [] 
			self.new_app.aux['choosing_photo']['friends_info'] = file_1

		


		self.new_app.add_frames( 'main_page' )
		position, size = self.new_app.making_pairs( 0, 0, Width, Height )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'main_page',
			name = 'bg_canvas',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)
		

		position, size = self.new_app.making_ralative_pairs( 28, 31, 356, 187 )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'main_page',
			name = 'info_canvas',
			path = 'resource/info_bg.png',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_ralative_pairs( 247+55-71-28, 69+55-55-31, 143, 110 )
		if not First_Use:
			self.new_app.create_photo_on_canvas(
				tar_frame = 'main_page',
				wid_name = 'info_canvas',
				tag =  'personal_img',
				path = self.new_app.aux['choosing_photo']['pic_path'],
				size = size,
				position = position
			)


		self.new_app.widgets['main_page']['info_canvas'].lift(
			'main' )
		position, size = self.new_app.making_ralative_pairs( 30, 30, 20, 0 )
		self.new_app.widgets[ 'main_page' ][ 'info_canvas' ].create_text(
			(position['x'],position['y']), fill = 'white', tags=['name','up'],
			text = self.new_app.aux[ 'choosing_photo' ][ 'user_name' ],
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) )

		position, size = self.new_app.making_ralative_pairs( 30, 70, 16, 0 )
		self.new_app.widgets[ 'main_page' ][ 'info_canvas' ].create_text(
			( position['x'], position['y'] ), fill = 'white', tags=['id','up'],
			text = 'I D : '+ str( np.random.randint( 999999, 9999999 ) ),
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		position, size = self.new_app.making_ralative_pairs( 30, 85, 16, 0 )
		self.new_app.widgets[ 'main_page' ][ 'info_canvas' ].create_text(
			( position['x'], position['y'] ), fill = 'white', tags=['late_time','up'],
			text = '遲到總時間：'+
				   str(int(self.new_app.aux[ 'choosing_photo' ][ 'late_time' ]/60 /60) ).zfill(2) +':'+
				   str(int(self.new_app.aux[ 'choosing_photo' ][ 'late_time' ]/60) ).zfill(2) +':'+
				   str(int(self.new_app.aux[ 'choosing_photo' ][ 'late_time' ]%60) ).zfill(2),
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		position, size = self.new_app.making_ralative_pairs( 30, 110, 10, 0 )
		self.new_app.widgets[ 'main_page' ][ 'info_canvas' ].create_text(
			( position['x'], position['y'] ), fill = 'white', tags=['late_time','up'],
			text = '你的人生遲到率',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		position, size = self.new_app.making_ralative_pairs( 30, 150, 10, 0 )
		self.new_app.widgets[ 'main_page' ][ 'info_canvas' ].create_text(
			( position['x'], position['y'] ), fill = 'white', tags=['late_time','up'],
			text = '遲到',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		position, size = self.new_app.making_ralative_pairs( 165, 150, 10, 0 )
		self.new_app.widgets[ 'main_page' ][ 'info_canvas' ].create_text(
			( position['x'], position['y'] ), fill = 'white', tags=['late_time','up'],
			text = '準時',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)


		if self.new_app.aux['choosing_photo']['ratio'] == 0 :
			position, size = self.new_app.making_ralative_pairs( 32, 128, 176, 142 )
			self.new_app.widgets['main_page']['info_canvas'].create_rectangle(
				position['x'], position['y'], size['w'], size['h'], fill = 'white',
				tags = [ 'late_ratio','up' ], width = 0
			)
			position, size = self.new_app.making_ralative_pairs( 106, 129, 106, 141 )
			self.new_app.widgets['main_page']['info_canvas'].create_line(
				position['x'], position['y'], size['w'], size['h'], fill = '#ECCE90',
				tags = [ 'late_ratio_bar','up' ], width = 1
			)
		else :
			print( 'here' )
			position, size = self.new_app.making_ralative_pairs( 32, 128, 32+144*self.new_app.aux['choosing_photo']['ratio'], 142 )
			self.new_app.widgets['main_page']['info_canvas'].create_rectangle(
				position['x'], position['y'], size['w'], size['h'], fill = '#F09696',
				tags = [ 'late_ratio','up' ], width = 0
			)
			position, size = self.new_app.making_ralative_pairs( 176-144*self.new_app.aux['choosing_photo']['ratio'], 128, 176, 142 )
			self.new_app.widgets['main_page']['info_canvas'].create_rectangle(
				position['x'], position['y'], size['w'], size['h'], fill = '#80DD79',
				tags = [ 'ontime_ratio','up' ], width = 0
			)
			position, size = self.new_app.making_ralative_pairs( 32+144*self.new_app.aux['choosing_photo']['ratio'], 129, 32+144*self.new_app.aux['choosing_photo']['ratio'], 141 )
			self.new_app.widgets['main_page']['info_canvas'].create_line(
				position['x'], position['y'], size['w'], size['h'], fill = '#ECCE90',
				tags = [ 'late_ratio_bar','up' ], width = 1
			)


		position, size = self.new_app.making_ralative_pairs( 30, 127, 151, 18 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name = 'info_canvas',
			size = size,
			path = 'resource/late_bar.png',
			position = position,
			tag = 'late_bar'
		)
		self.new_app.widgets[ 'main_page' ][ 'info_canvas' ].itemconfig(
			'late_bar', tags = ['late_bar','up'] )



		position, size = self.new_app.making_ralative_pairs( 30, 238, 356, 378 )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'main_page',
			name  = 'active_canvas',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		if self.new_app.aux['choosing_photo']['active'] == 0 :
			position, size = self.new_app.making_ralative_pairs( 97, 387-238 , 24, 0 )
			self.new_app.widgets[ 'main_page' ][ 'active_canvas' ].create_text(
				( position['x'], position['y'] ), fill = '#F0CD95', tags='nono_text',
				text = '按+建立新活動',
				anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
			)
		else:
			##TODO
			pass


		position, size = self.new_app.making_ralative_pairs( 0, 624, 414, 109 )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'main_page',
			name  = 'setting_canvas',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_ralative_pairs( 0, 660-624, 213, 78 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name = 'setting_canvas',
			size = size,
			path = 'resource/friends_setting.png',
			position = position,
			tag = 'friends_setting'
		)

		position, size = self.new_app.making_ralative_pairs( 206, 660-624, 213, 78 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name = 'setting_canvas',
			size = size,
			path = 'resource/setting_setting.png',
			position = position,
			tag = 'setting_setting'
		)

		position, size = self.new_app.making_ralative_pairs( 168, 0, 78, 78 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name = 'setting_canvas',
			size = size,
			path = 'resource/add.png',
			position = position,
			tag = 'add_setting'
		)

		self.new_app.add_frames( 'setting_page' )

		position, size = self.new_app.making_pairs( 0, 0, Width, Height )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'setting_page',
			name = 'main_canvas',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_ralative_pairs( 20, 20, 40, 30 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'setting_page',
			wid_name  = 'main_canvas',
			path = 'resource/home.png',
			tag = 'home_icon',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 62, 120, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'setting_page',
			wid_name  = 'main_canvas',
			path = 'resource/personal_setting.png',
			tag = 'personal_setting',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 62, 209, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'setting_page',
			wid_name  = 'main_canvas',
			path = 'resource/about.png',
			tag = 'about_setting',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 62, 298, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'setting_page',
			wid_name  = 'main_canvas',
			path = 'resource/language_setting.png',
			tag = 'language_setting',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 62, 387, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'setting_page',
			wid_name  = 'main_canvas',
			path = 'resource/notifiction.png',
			tag = 'notifictione_setting',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 62, 476, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'setting_page',
			wid_name  = 'main_canvas',
			path = 'resource/friend_setting.png',
			tag = 'friend_setting',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 62, 565, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'setting_page',
			wid_name  = 'main_canvas',
			path = 'resource/rapping.png',
			tag = 'rapping_setting',
			size = size,
			position = position
		)


		## personal_page
		self.new_app.add_frames( 'personal_page' )
		position, size = self.new_app.making_pairs( 0, 0, Width, Height )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'personal_page',
			name = 'main_canvas',
			size =size, 
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_ralative_pairs( 16, 20, 27, 15 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'personal_page',
			wid_name = 'main_canvas',
			size = size,
			position = position,
			path = 'resource/photo_config_back.png',
			tag = 'back'
		)

		position, size = self.new_app.making_ralative_pairs( 19, 105, 20, 0 )
		self.new_app.widgets['personal_page']['main_canvas'].create_text(
				( position['x'], position['y'] ), fill = '#F1B696', tags='header_text',
				text = '個人設定',
				anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		
		position, size = self.new_app.making_ralative_pairs( 28, 195, 364, 207 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'personal_page',
			wid_name = 'main_canvas',
			size = size,
			position = position,
			path = 'resource/lazy.png',
			tag = 'entries'
		)


		### about_page
		self.new_app.add_frames( 'about_page' )
		position, size = self.new_app.making_pairs( 0, 0, Width, Height )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'about_page',
			name = 'main_canvas',
			size =size, 
			position = position,
			bg = '#FAF8E1'
		)
		
		position, size = self.new_app.making_ralative_pairs( 16, 20, 27, 15 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'about_page',
			wid_name = 'main_canvas',
			size = size,
			position = position,
			path = 'resource/photo_config_back.png',
			tag = 'back'
		)
		position, size = self.new_app.making_ralative_pairs( 41, 102, 20, 0 )
		self.new_app.widgets[ 'about_page' ][ 'main_canvas' ].create_text(
			(position['x'],position['y']), fill = '#F1B696', tags='header_text',
			text = '關於xxx',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)
		position, size = self.new_app.making_ralative_pairs( 133, 235, 20, 0 )
		self.new_app.widgets[ 'about_page' ][ 'main_canvas' ].create_text(
			(position['x'],position['y']), fill = '#F1B696', tags='version_text',
			text = '使用版本 1.00.0',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		position, size = self.new_app.making_ralative_pairs( 62, 299, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'about_page',
			wid_name  = 'main_canvas',
			path      = 'resource/phonw_setting.png',
			tag = 'phone_setting',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 62, 391, 293, 51 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'about_page',
			wid_name  = 'main_canvas',
			path      = 'resource/service.png',
			tag = 'service_rule',
			size = size,
			position = position
		)

		position, size = self.new_app.making_pairs( Width, -Height, Width*2, Height*2 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name  = 'info_canvas',
			path = 'resource/gray_back.png',
			tag = 'gray',
			size =size,
			position = position
		)
		#self.new_app.widgets['main_page']['info_canvas'].lower('gray')
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name  = 'active_canvas',
			path = 'resource/gray_back.png',
			tag = 'gray',
			size =size,
			position = position
		)
		#self.new_app.widgets['main_page']['active_canvas'].lower('gray')
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name  = 'setting_canvas',
			path = 'resource/gray_back.png',
			tag = 'gray',
			size =size,
			position = position
		)
		#self.new_app.widgets['main_page']['setting_canvas'].lower('gray')
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name  = 'bg_canvas',
			path = 'resource/gray_back.png',
			tag = 'gray',
			size =size,
			position = position
		)
		#self.new_app.widgets['main_page']['bg_canvas'].lower('gray')
		position, size = self.new_app.making_ralative_pairs( Width, 0, 296, 188 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'main_page',
			wid_name  = 'active_canvas',
			path = 'resource/error_nofriend.png',
			tag = 'messenge',
			size =size,
			position = position
		)


		#### adding friend page

		position, size = self.new_app.making_ralative_pairs( 0, 0, Width, 85 )
		self.new_app.add_frames( "adding_friend" )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'adding_friend',
			name = 'header_canvas',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_ralative_pairs( 21, 21, 35, 27 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'adding_friend',
			wid_name = 'header_canvas',
			tag = 'home',
			path = 'resource/home.png',
			size = size,
			position = position
		)
		position, size = self.new_app.making_ralative_pairs( 165, 33, 21, 0 )
		self.new_app.widgets[ 'adding_friend' ][ 'header_canvas' ].create_text(
			(position['x'],position['y']), fill = '#F1B696', tags='header_text',
			text = '好友列表',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		position, size = self.new_app.making_ralative_pairs( 0, 85, 414, 533-85 ) 
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'adding_friend',
			name = 'list_canvas',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_pairs( 0, 0, Width, 0 ) 
		self.new_app.widgets[ 'adding_friend' ][ 'list_canvas' ].create_line(
			position['x'], position['y'], size['w'], size['h'], fill = '#F0CD95',
			tags = 'line', width = 1
		)

		if self.new_app.aux['choosing_photo']['friends'] == 0 :
			position, size = self.new_app.making_ralative_pairs( 63, 255-85, 24, 0 ) 
			self.new_app.widgets[ 'adding_friend' ][ 'list_canvas' ].create_text(
			(position['x'],position['y']), fill = '#F1B696', tags='header_text',
			text = '目前無好友～快去新增吧！',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) )
			)
		else :
			#TODO
			pass

		position, size = self.new_app.making_ralative_pairs( 0, 532, Width, Height-532 ) 
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'adding_friend',
			name = 'adding_canvas',
			size = size,
			position = position,
			bg = '#FAF8E1'
		)

		position, size = self.new_app.making_ralative_pairs( 44, 0, 18, 0 ) 
		self.new_app.widgets[ 'adding_friend' ][ 'adding_canvas' ].create_text(
			(position['x'],position['y']), fill = '#F1B696', tags='header_text',
			text = '還不是好友？',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) )
		)

		position, size = self.new_app.making_ralative_pairs( 42, 580-532, 83, 83 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'adding_friend',
			wid_name  = 'adding_canvas',
			path = 'resource/ID_but.png',
			tag = 'ID_but',
			size = size,
			position = position
		)
		position, size = self.new_app.making_ralative_pairs( 165, 580-532, 83, 83 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'adding_friend',
			wid_name  = 'adding_canvas',
			path = 'resource/QR_but.png',
			tag = 'QR_but',
			size = size,
			position = position
		)
		position, size = self.new_app.making_ralative_pairs( 288, 580-532, 83, 83 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'adding_friend',
			wid_name  = 'adding_canvas',
			path = 'resource/Sreach_but.png',
			tag = 'Sreach_but',
			size = size,
			position = position
		)

		## ID Sreach Page
		self.new_app.add_frames( "ID_page" )

		position, size = self.new_app.making_pairs( 0, 0, Width, Height )
		self.new_app.add_labels_with_image(
			type = 'canvas',
			tar_name = 'ID_page',
			name = 'main_canvas',
			bg = '#FAF8E1',
			size =size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 16, 20, 27,15 )
		self.new_app.create_photo_on_canvas(
			tar_frame = 'ID_page',
			wid_name = 'main_canvas',
			path = 'resource/photo_config_back.png',
			tag = 'back',
			size = size,
			position = position
		)

		position, size = self.new_app.making_ralative_pairs( 13, 64, 21, 0 )
		self.new_app.widgets[ 'ID_page' ][ 'main_canvas' ].create_text(
			(position['x'],position['y']), fill = '#F1B696', tags='header_text',
			text = 'ID搜尋好友',
			anchor = 'nw', font = ( "Segoe UI.ttf" , str( size['w'] ) ) 
		)

		position, size = self.new_app.making_ralative_pairs( 0, 113, 414, 113 )
		self.new_app.widgets['ID_page']['main_canvas'].create_line(
			position['x'], position['y'], size['w'], size['h'], fill = '#F0CD95',
			tags = 'bar', width = 1
		)

		##TODO










		

		

class new_app( object ):
	def __init__(self, main_obj ,target, state ):
		self.main_obj = main_obj
		self.frames = {}
		self.resource = {}
		self.widgets  = {}
		self.aux = {}
	def add_frames( self, name ):
		frame = tk.Frame( self.main_obj.container )
		frame.grid( row=0, column=0, sticky="nsew" )
		self.frames[ name ] = frame 
		self.resource[ name ] = {}
		self.widgets[ name ] = {}
		self.aux[ name ] = {}
	def add_labels_with_image( self,type, tar_name, name, path=None, size={'w':0 , 'h':0 }, position={'x':0 , 'y':0 },bg = 'white', func=None, show_mark=None, act='<Button-1>' ):
		if type == 'label':
			self.widgets[ tar_name ][ name ]=tk.Label( self.frames[ tar_name ] )
			self.widgets[ tar_name ][ name ].config(padx=0, pady=0)
		elif type == 'entry':
			self.widgets[ tar_name ][ name ] = tk.Entry( self.frames[tar_name] )
			if show_mark :
				self.widgets[ tar_name ][ name ].config( show = show_mark )
		elif type == 'canvas':
			self.widgets[ tar_name ][ name ] = tk.Canvas( self.frames[tar_name] )
			if path:
				self.resource[ tar_name ][ name+'pic' ] = Image.open( path ).resize( (size['w'], size['h']), Image.ANTIALIAS  )
				self.resource[ tar_name ][ name+'pic' ] = ImageTk.PhotoImage(  self.resource[ tar_name ][ name+'pic' ] )
				self.widgets[ tar_name ][ name ].create_image( (0,0),image=self.resource[ tar_name ][ name+'pic' ] , tag='main', anchor='nw' )
		
		if path and not type == 'canvas' :
			self.resource[ tar_name ][ name+'pic' ] = Image.open( path ).resize( (size['w'], size['h']), Image.ANTIALIAS  )
			self.resource[ tar_name ][ name+'pic' ] = ImageTk.PhotoImage(  self.resource[ tar_name ][ name+'pic' ] )
			self.widgets[ tar_name ][ name ].config(  image=self.resource[ tar_name ][ name+'pic' ] )
		self.widgets[ tar_name ][ name ].config(  bg=bg, highlightthickness=0, bd=0, border=0 )
		self.widgets[ tar_name ][ name ].place( x=position['x'], y=position['y'], width=size['w'], height=size['h'] )
		if func != None:
			self.widgets[ tar_name ][ name ].bind( act, func )
		self.frames[ tar_name ].update()
	def making_pairs( self, x, y, width, height ):
		return { 'x':x, 'y':y } , { 'w':width, 'h':height }
	def making_ralative_pairs( self, x, y, width, height ):
		return { 'x':int( x/414*Width), 'y':int( y/736*Height) } , { 'w':int( width/414*Width) , 'h':int( height/736*Height) } 
	def show( self, tar_show , setfocus = None, condition=False ):
		for i in tar_show :
			self.frames[ i ].tkraise()
		#print( 'here1' )
		if not setfocus == None:
			#print( 'here2' )
			setfocus.focus_set()
		if condition :
			condition = True
	def change_photo( self, tar_frame, wid_name, new_path, condition=True ):
		if condition:
			self.resource[ tar_frame ][ wid_name+'pic' ] = Image.open( new_path ).resize( (self.widgets[ tar_frame ][ wid_name ].winfo_width(), self.widgets[ tar_frame ][ wid_name ].winfo_height()), Image.ANTIALIAS  )
			self.resource[ tar_frame ][ wid_name+'pic' ] = ImageTk.PhotoImage(  self.resource[ tar_frame ][ wid_name+'pic' ] )
			self.widgets[ tar_frame ][ wid_name ].config(  image=self.resource[ tar_frame ][ wid_name+'pic' ] )
	def setting_var( self, tar_frame, type, name, var ) :
		if type == 'aux' :
			self.aux[ tar_frame ][ name ] = var
		elif type == resource:
			self.resource[ tar_frame ][ name ] = var
		elif type == frames:
			self.frames[ tar_frame ] = var
		elif type == resource:
			self.resource[ tar_frame ][ name ] = var
		elif type == widgets:
			self.widgets[ tar_frame ][ name ] = var

	def create_photo_on_canvas( self, tar_frame, wid_name, path=None, tag=None, size={ 'w':0, 'h':0 }, position={ 'x':0, 'y':0 } ) :
		if path:
			self.aux[  tar_frame ][ wid_name+tag+'path' ] = path
			self.resource[ tar_frame ][ wid_name+tag+'pic' ] = Image.open( path ).resize( (size['w'],size['h']), Image.ANTIALIAS  )
			self.resource[ tar_frame ][ wid_name+tag+'pic' ] = ImageTk.PhotoImage(  self.resource[ tar_frame ][ wid_name+tag+'pic' ] )
		self.widgets[ tar_frame ][ wid_name ].create_image( (position['x'],position['y']),tag=tag, image=self.resource[ tar_frame ][ wid_name+tag+'pic' ], anchor='nw' )
		
	def move_phote_on_canvas( self, tar_frame, wid_name, tag, position={'x':0, 'y':0} ):
		self.widgets[ tar_frame ][ wid_name ].coords( self.widgets[ tar_frame ][ wid_name ].find_withtag( tag )[0], ( position['x'], position['y'] ) )
		
	def make_draggable( self, tar_frame, wid_name, limit_height ):
	    self.widgets[ tar_frame ][ wid_name ].bind("<Button-1>", lambda event : self.on_drag_start( event , tar_frame = tar_frame , wid_name=wid_name ) )
	    self.widgets[ tar_frame ][ wid_name ].bind("<B1-Motion>", lambda event : self.on_drag_motion( event ,  tar_frame = tar_frame , wid_name=wid_name, limit_height=limit_height ) )
	    self.aux[ tar_frame ][ wid_name ] = { 'on_drag_start_x':0, 'on_drag_start_y':0 }

	def on_drag_start(self, event, tar_frame, wid_name ):
		self.aux[ tar_frame ][ wid_name ][ 'on_drag_start_x' ] = event.x
		self.aux[ tar_frame ][ wid_name ][ 'on_drag_start_y' ] = event.y
	def on_drag_motion(self, event, tar_frame, wid_name, limit_height ):
		x = self.widgets[ tar_frame ][ wid_name ].winfo_x() - self.aux[ tar_frame ][ wid_name ][ 'on_drag_start_x' ] + event.x
		y = self.widgets[ tar_frame ][ wid_name ].winfo_y() - self.aux[ tar_frame ][ wid_name ][ 'on_drag_start_y' ] + event.y
		#print( y )
		#print( limit_height )
		if y < -10 and y>-1*limit_height :
			self.widgets[ tar_frame ][ wid_name ].place( y=y )

class app( tk.Frame ):
	"""docstring for app"""
	def __init__(self, main_obj ,target, state ):

		self.main_obj = main_obj

		super(app, self).__init__( main_obj.container )
		self.grid(row=0, column=0, sticky="nsew")

		self.resource = {}
		self.widgets  = {}

		self.log_check = False

		if state == 'loading':
			self.loading()
	def loading( self ):
		step = 5
		self.resource[ 'loading_image_0' ] = Image.open( 'resource/loading0.png' )
		self.resource[ 'loading_image_0' ] = self.resource[ 'loading_image_0' ].resize((Width,Height),Image.ANTIALIAS )
		self.resource[ 'loading_image_0' ] = ImageTk.PhotoImage( self.resource[ 'loading_image_0' ] )
		self.resource[ 'loading_image_1' ] = Image.open( 'resource/loading1.png' )
		self.resource[ 'loading_image_1' ] = self.resource[ 'loading_image_1' ].resize((Width,Height),Image.ANTIALIAS )
		self.resource[ 'loading_image_1' ] = ImageTk.PhotoImage( self.resource[ 'loading_image_1' ] )
		self.resource[ 'loading_image_2' ] = Image.open( 'resource/loading2.png' )
		self.resource[ 'loading_image_2' ] = self.resource[ 'loading_image_2' ].resize((Width,Height),Image.ANTIALIAS )
		self.resource[ 'loading_image_2' ] = ImageTk.PhotoImage( self.resource[ 'loading_image_2' ] )
		self.resource[ 'loading_image_3' ] = Image.open( 'resource/loading3.png' )
		self.resource[ 'loading_image_3' ] = self.resource[ 'loading_image_3' ].resize((Width,Height),Image.ANTIALIAS )
		self.resource[ 'loading_image_3' ] = ImageTk.PhotoImage( self.resource[ 'loading_image_3' ] )
		self.widgets[ 'background' ] = tk.Label( self, image = self.resource[ 'loading_image_0' ] ,compound = None , bd =0, border=0 )
		self.widgets[ 'background' ].place( x=0 , y=0 )
		self.update()
		for i in range( step ):
			time.sleep(0.3)
			num = str( i%3 )
			name = 'loading_image_'+num
			self.widgets[ 'background' ] = tk.Label( self, image = self.resource[ name ] ,compound = None , bd =0, border=0 )
			self.widgets[ 'background' ].place( x=0 , y=0 )
			self.update()
		if First_Use:
			self.log()
		else :
			## TODO
			file = np.load( 'resource/user.npz'  )
			self.main_obj.new_app.aux['choosing_photo']['late_time'] = file['time']
			self.main_obj.new_app.aux['choosing_photo']['user_name'] = str(file['user_name'])
			self.main_obj.new_app.aux['choosing_photo']['pic_path'] = str(file['pic_path'])
			self.main_obj.new_app.aux['choosing_photo']['friends'] = int(file['friends'])
			self.main_obj.new_app.aux['choosing_photo']['friends_list'] = [] 
			self.main_obj.new_app.aux['choosing_photo']['ratio'] = file['ratio']
			self.main_obj.new_app.aux['choosing_photo']['active'] = file['active']
			self.main_obj.new_app.show( [ 'main_page' ] )

			file_1 = np.load( 'resource/friends.npz' )
			self.main_obj.new_app.aux['choosing_photo']['friends_info'] = file_1



			
	def log( self ):
		self.entry_position = { 'x':int( (72+60)/414*Width), 'y':int(359/736*Height) }
		self.entry_size     = { 'x':int( (273-68)/414*Width), 'y':int( 34/736*Height) }

		self.checkbox_position = { 'x':int( 72/414*Width), 'y':int( 435/736*Height) }
		self.checkbox_size     = { 'x':int( 20/414*Width), 'y':int( 20/736*Height) }
		self.checkmark_size	   = { 'x':int( 10/414*Width), 'y':int( 19/736*Height) }

		rule_position = { 'x':int( 248/414*Width), 'y':int(433/736*Height) }
		rule_size = { 'x':int( 96/414*Width), 'y':int( 22/736*Height) }

		self.main_obj.state = 'log'
		self.resource[ 'log_image' ] = Image.open( 'resource/phone_log.png' ).resize((Width,Height),Image.ANTIALIAS )
		self.resource[ 'log_image' ] = ImageTk.PhotoImage( self.resource[ 'log_image' ] )
		self.widgets[ 'log_background' ] = tk.Label( self, image=self.resource['log_image'], compound=None, bd=0, border=0 )
		self.widgets[ 'log_background' ].place( x=0, y=0 )
		self.widgets[ 'phone_entry' ] = tk.Entry( self, bd=0, border=0, highlightthickness=0 )
		self.widgets[ 'phone_entry' ].config( font = ( "Times" , int( 20 /1.5* ( Width/250 ) ) ) )
		self.widgets[ 'phone_entry' ].place( x=self.entry_position['x'], y=self.entry_position['y'], anchor='nw', height=self.entry_size['y'], width=self.entry_size['x'] )
		self.widgets[ 'phone_entry' ].focus_set()
		self.resource[ 'checkmark' ] = Image.open( 'resource/check-mark-icon.jpg' ).resize((self.checkmark_size['x'],self.checkmark_size['y']),Image.ANTIALIAS )
		self.resource[ 'checkmark' ] = ImageTk.PhotoImage(self.resource[ 'checkmark' ])
		self.widgets[ 'checkbox' ] = tk.Label( self )
		self.widgets[ 'checkbox' ].place( x=self.checkbox_position['x'], y=self.checkbox_position['y'], anchor='nw', height=self.checkbox_size['x'], width=self.checkbox_size['y'] )
		self.widgets[ 'checkbox' ].bind( '<Button-1>', self.show_mark )
		self.resource[ 'blank' ] =  Image.open( 'resource/rule.png' ).resize( ( rule_size['x'],rule_size['y']) ,Image.ANTIALIAS  )
		self.resource[ 'blank' ] = ImageTk.PhotoImage( self.resource[ 'blank' ] )
		self.widgets[ 'rules' ] = tk.Label( self, image=self.resource[ 'blank' ], bg = '#FAF8E1' )
		self.widgets[ 'rules' ].place( x=rule_position['x'], y=rule_position['y'], anchor='nw' )
		self.widgets[ 'rules' ].bind( '<Button-1>', self.show_rule )

		go_position = { 'x':int(119/414*Width),'y':int(514/736*Height) }
		go_size = { 'x':int(180/414*Width),'y':int(50/736*Height) }
		self.resource[ 'Go_pic' ] = Image.open( 'resource/password.png' ).resize( ( go_size['x'],go_size['y'] ),Image.ANTIALIAS  )
		self.resource[ 'Go_pic' ] = ImageTk.PhotoImage( self.resource[ 'Go_pic' ] )
		self.widgets[ 'Go_button' ] = tk.Label( self, image=self.resource[ 'Go_pic' ],bd=0, highlightthickness=0, padx=0, pady=0 )
		self.widgets[ 'Go_button' ].place( x=go_position['x'], y=go_position['y'], anchor='nw' )
		print( (self.main_obj.root.winfo_geometry()) )
		
		
		if DEBUG:
			self.widgets[ 'Go_button' ].bind( '<Button-1>', self.key_password )
		if not DEBUG:
			size = { 'W':int(178/414*Width),'H':int(82/736*Height) }
			self.widgets[ 'Go_button' ].bind( '<Button-1>',
			lambda event, name = 'resource/Error_phone.png' ,size = size: self.show_error( name,size ) )
			
		
		while True:
			if len(self.widgets[ 'phone_entry' ].get()) < 10 or not self.log_check:
				self.update()
			else:
				if self.log_check and len(self.widgets[ 'phone_entry' ].get()) >= 10:
					self.resource[ 'Go_pic' ] = Image.open( 'resource/password_ready.png' ).resize( ( go_size['x'],go_size['y'] ),Image.ANTIALIAS  )
					self.resource[ 'Go_pic' ] = ImageTk.PhotoImage( self.resource[ 'Go_pic' ] )
					self.widgets[ 'Go_button' ].config( image=self.resource[ 'Go_pic' ],bd=0, highlightthickness=0, padx=0, pady=0 )
					self.widgets[ 'Go_button' ].unbind("<Button 1>")
					self.widgets[ 'Go_button' ].bind( '<Button-1>', self.key_password )
					self.update()
					break
		self.update()

	def show_error( self, name, size ):

		self.img_img = grab( region=( 
			self.winfo_rootx()*shotratio,
			self.winfo_rooty()*shotratio, 
			self.winfo_width()*shotratio, 
			self.winfo_height()*shotratio ) )
		self.img_img = np.uint8( self.img_img )
		self.img_img = Image.fromarray( np.uint8(self.img_img/2) ).resize( (Width, Height), Image.ANTIALIAS )
		# self.img.show()
		self.img_img = ImageTk.PhotoImage( self.img_img )
		self.img = tk.Label( self, image = self.img_img, bd =0 ,border=0 ,highlightthickness=0, padx=0 ,pady=0 )
		#img.place( x=0, y=0 )

		self.error_img = Image.open( name ).resize( (size['W'], size['H']), Image.ANTIALIAS )
		self.error_img = ImageTk.PhotoImage( self.error_img )
		self.error = tk.Label( self, image= self.error_img, bd =0 ,border=0 ,highlightthickness=0, padx=0 ,pady=0, bg=_from_rgb( (188,188,182) ) )

		self.img.place( x=0, y=0, height=Height, width=Width )
		self.error.place( relx=0.5, rely=0.5, anchor='center' )
		self.img.bind( '<Button-1>', lambda event, dis=[self.img,self.error]:self.deshow_error( dis ) )
		self.update()
	def deshow_error( self,  dis ):
		for i in dis:
			i.place( x=Width, y=0 )
		self.update()

	def key_password( self, event ):
		self.password = np.random.randint(99999,999999)
		self.number = 0
		print( self.password )
		self.resource[ 'password_image' ] = Image.open( 'resource/enter.png' ).resize( ( Width, Height ),Image.ANTIALIAS  )
		self.resource[ 'password_image' ] = ImageTk.PhotoImage( self.resource[ 'password_image' ] )
		self.widgets[ 'Go_button' ] = tk.Label( self, image=self.resource[ 'password_image' ] , bd=0, border=0 )
		self.widgets[ 'Go_button' ].place( x=0, y=0, anchor='nw' )

		first_entry_position = { 'x':int(113/414*Width),'y':int(368/736*Height) }
		entry_size = { 'x':int(22/414*Width),'y':int(15/736*Height) }
		entry_side = int(12/414*Width)
		self.widgets[ 'enter_entry_list' ] = []
		self.Value = []
		for i in range( 6 ):
			self.Value.append( tk.StringVar() )
			self.widgets[ 'enter_entry_list' ].append( tk.Entry( self,bg='#FAF8E1', bd=0, border=0, highlightthickness=0, textvariable=self.Value[i], justify='center' ) )
			self.widgets[ 'enter_entry_list' ][i].place( x=first_entry_position['x']+i*( entry_size['x']+entry_side ) ,
														 y=first_entry_position['y'],
														 width = entry_size['x'],
														 height= entry_size['y'],
														 anchor='nw' )
			self.widgets[ 'enter_entry_list' ][i].bind( '<BackSpace>', self.back )
			self.widgets[ 'enter_entry_list' ][i].bind( '<Key>', self.forward )

		done_position = { 'x':int(159/414*Width),'y':int(514/736*Height) }
		done_size = { 'x':int(100/414*Width),'y':int(48/736*Height) }
		self.resource[ 'done_image' ] = Image.open( 'resource/Done.png' ).resize( ( done_size['x'], done_size['y'] ),Image.ANTIALIAS  )
		self.resource[ 'done_image' ] = ImageTk.PhotoImage( self.resource[ 'done_image' ] )
		self.widgets[ 'done_image' ] = tk.Label( self, image=self.resource[ 'done_image' ] ,bg = '#FAF8E1', bd=0, border=0 )
		self.widgets[ 'done_image' ].place( x =done_position['x'], y =done_position['y'] )
		
		self.widgets[ 'done_image' ].bind( '<Button-1>', lambda event, number=self.Value, tar=self.password :self.main_obj.call_new_app(number, tar) )
		

		self.update()
		self.now = 0
		self.widgets['enter_entry_list'][self.now].focus_set()
		self.update()

	def forward( self, event ):
		if len(self.Value[self.now].get())>=1:
			self.widgets['enter_entry_list'][self.now].delete(0,1)
		if self.now < 5:
			#print( self.Value[self.now].get() )
			self.now += 1
			self.widgets['enter_entry_list'][self.now].focus_set()
			self.update()
	def back( self, event ):
		if len(self.Value[self.now].get())>=1:
			self.widgets['enter_entry_list'][self.now].delete(0,1)
		if self.now > 0:
			#print( self.Value[self.now].get() )
			self.widgets['enter_entry_list'][self.now].delete(0 ,len(self.Value[self.now].get()) )
			self.now -= 1
			self.widgets['enter_entry_list'][self.now].focus_set()
			self.update()

		

	def show_rule( self, event ):
		# print( 'still valid' )
		rule_size = { 'x':int( 308/414*Width), 'y':int(482/736*Height) }
		self.resource[ 'rules_image' ] = Image.open( 'resource/balabala.png' ).resize((rule_size['x'],rule_size['y']),Image.ANTIALIAS )
		self.resource[ 'rules_image' ] = ImageTk.PhotoImage( self.resource[ 'rules_image' ] )
		'''
		self.resource[ 'rules_bg_image' ] = np.uint8(pyscreeze.screenshot(region=( self.main_obj.root.winfo_x()+1, self.main_obj.root.winfo_y()+70, Width*2, Height*2)))
		
		self.resource[ 'rules_bg_image' ] = Image.fromarray( np.uint8(self.resource[ 'rules_bg_image' ]/2)  ).resize( (Width,Height),Image.ANTIALIAS   )
		#self.resource[ 'rules_bg_image' ].show( )
		self.resource[ 'rules_bg_image' ] = ImageTk.PhotoImage( self.resource[ 'rules_bg_image' ] )
		'''
		self.widgets[ 'bk' ] = tk.Label( self, bg ='#C8C7B4',bd=0 , border=0, highlightthickness=0, padx=0, pady=0 )
		self.widgets[ 'bk' ].place( x=0, y=0, height=Height, width= Width, anchor='nw' )
		self.widgets[ 'rules_box' ] = tk.Label( self , image = self.resource[ 'rules_image' ], bg ='#C8C7B4',bd=0 , border=0, highlightthickness=0, padx=0, pady=0  )
		self.widgets[ 'rules_box' ].place(relx=0.5, rely=0.5, anchor='center')

		self.widgets[ 'bk' ].bind( '<Button-1>', self.deshow_rule )

		self.update()
		return
	def deshow_rule( self, event ):
		## TODO
		# here to cancel the rule
		# back to logging interface
		self.widgets[ 'log_background' ].tkraise()
		self.widgets[ 'rules' ].tkraise()
		self.widgets[ 'checkbox' ].tkraise()
		self.widgets[ 'phone_entry' ].tkraise()
		self.widgets[ 'Go_button' ].tkraise()
		return 

	def show_mark( self, event ):
		# print( 'here' )
		if not self.log_check:
			self.widgets[ 'checkbox' ].config( image = self.resource[ 'checkmark' ]  )
			self.widgets[ 'checkbox' ].place( x=self.checkbox_position['x'], y=self.checkbox_position['y'], anchor='nw', height=self.checkbox_size['x'], width=self.checkbox_size['y'] )
			self.update()
			self.log_check = True
			# print( 'toggle true' )
		else :
			self.widgets[ 'checkbox' ].config( image ='' )
			self.widgets[ 'checkbox' ].place( x=self.checkbox_position['x'], y=self.checkbox_position['y'], anchor='nw', height=self.checkbox_size['x'], width=self.checkbox_size['y'] )
			self.update()
			self.log_check = False
			# print( 'toggle false' )

class outside( tk.Frame ):
	def __init__(self, main_obj, target):
		self.main_obj = main_obj
		self.button_position = { 'x':int( 41/(414/Width)), 'y':int(418/(736/Height)) }
		self.button_size     = { 'x':int( 62/(414/Width)), 'y':int( 62/(736/Height)) }

		print( self.button_position['x'], self.button_position['y'] )
		super(outside, self ).__init__( main_obj.container, border=0, bd=0, highlightthickness=0 )
		self.grid(row=0, column=0, sticky="nsew" )

		self.widgets = {}


		self.widgets[ 'bg_image' ] = Image.open( 'resource/outside.png' )
		self.widgets[ 'bg_image' ] = self.widgets[ 'bg_image' ].resize((Width,Height),Image.ANTIALIAS )
		self.widgets[ 'bg_image' ] = ImageTk.PhotoImage( self.widgets[ 'bg_image' ] )
		self.widgets[ 'background' ] = tk.Label( self, image=self.widgets['bg_image'] ,compound = None , bd =0, border=0,padx=0, pady=0, highlightthickness=0)
		self.widgets[ 'background' ].pack()
		self.widgets[ 'bt_image' ] = Image.open( 'resource/AppButton.png' )
		# self.widgets[ 'bt_image' ].show()
		
		self.widgets[ 'bt_image_resize' ] = self.widgets[ 'bt_image' ].resize((self.button_size['x'],self.button_size['y']),Image.ANTIALIAS )
		self.widgets[ 'bt_image_resize' ] = ImageTk.PhotoImage( self.widgets[ 'bt_image_resize' ] )

		self.widgets[ 'button' ] = tk.Label( self, image=self.widgets['bt_image_resize'], borderwidth=0, highlightthickness=0,padx=0,pady=0 )
		self.widgets[ 'button' ].bind( '<Button-1>', self.show_app )
		self.widgets[ 'button' ].place( x = self.button_position['x'], y =  self.button_position['y'], anchor= 'nw' )


		print('init')
	def show_app( self, event ):
		step = 10
		posx = self.button_position['x']
		posy = self.button_position['y']
		W   = self.button_size['x']
		H   = self.button_size['y']
		cut = 5

		for i in range( step ):
			time.sleep(0.01)
			posx = int(posx - self.button_position['x']/step)
			posy = int(posy - self.button_position['y']/step)
			W = int( W + Width/step )
			H = int( H + Height/step )
			if i < cut:
				self.widgets[ 'bt_image_resize' ] = self.widgets[ 'bt_image' ].resize((W,H),Image.ANTIALIAS )
				self.widgets[ 'bt_image_resize' ] = ImageTk.PhotoImage( self.widgets[ 'bt_image_resize' ] )
				self.widgets[ 'button' ].config( image = self.widgets[ 'bt_image_resize' ] )
			else:
				self.widgets[ 'bt_image_resize' ] = self.widgets[ 'bt_image' ].resize((1,1),Image.ANTIALIAS )
				self.widgets[ 'bt_image_resize' ] = ImageTk.PhotoImage( self.widgets[ 'bt_image_resize' ] )
				self.widgets[ 'button' ].config( image=self.widgets[ 'bt_image_resize' ]  ,  bg = 'black' ,height = H , width=W )
			
			#print( H, W )
			self.widgets[ 'button' ].place( x=posx, y=posy, anchor='nw' )
			self.update()
		self.widgets[ 'button' ].bind( '<Button-1>', '' )
		self.main_obj.state = 'loading'

		self.main_obj.app.tkraise()
		self.main_obj.app.loading()

def main():
	Main = window()

if __name__ == '__main__':
	main()
