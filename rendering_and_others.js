function CLASS_resources(){
// Private:
	let that = this;
	let resources_loaded = 0;
	let already_loading = false;
	
	function on_loaded(){
		resources_loaded++;
	};
// Public:
	this.images = new Array();
	this.sounds = new Array();
	this.levels = EXTERNAL_LEVELS;// External loading

	this.ready = function(){
		return (resources_loaded == NUM_RESOURCES);
	}
	this.load = function(){
		if(already_loading){
			return;
		}
		already_loading = true;
		////////////////////////////////////////////////////////
		// Images: /////////////////////////////////////////////
		////////////////////////////////////////////////////////
		// Background image
		that.images[0] = new Image();
		that.images[0].onload = on_loaded();
		that.images[0].src = IMAGE_DIR+"background.png";

		// Entry Image
		that.images[1] = new Image();
		that.images[1].onload = on_loaded();
		that.images[1].src = IMAGE_DIR+"entry.png";

		for(let i = 0; i < 9; i++){// From 2 to 10 garbage
			that.images[2+i] = new Image();
			that.images[2+i].onload = on_loaded();
			that.images[2+i].src = IMAGE_DIR+"garbage_"+i+".png";
		}

		for(let i = 0; i < 11; i++){// From 11 to 21 digits
			that.images[11+i] = new Image();
			that.images[11+i].onload = on_loaded();
			that.images[11+i].src = IMAGE_DIR+"digits_"+i+".png";
		}

		for(let i = 0; i < 3; i++){// From 22 to 30 buttons
			for(let j = 0; j < 3; j++){
				that.images[22+3*i+j] = new Image();
				that.images[22+3*i+j].onload = on_loaded();
				that.images[22+3*i+j].src = IMAGE_DIR+"userbutton_"+i+"-"+j+".png";
			}
		}

		for(let i = 0; i < 9; i++){// From 31 to 39 stones
			that.images[31+i] = new Image();
			that.images[31+i].onload = on_loaded();
			that.images[31+i].src = IMAGE_DIR+"stone_"+i+".png";
		}
		
		// Number 40 contains no image due to a miscalculation

		for(let i = 0; i < 6; i++){// From 41 to 58 doors
			for(let j = 0; j < 3; j++){// Reversed order for ease of access
				that.images[41+3*i+j] = new Image();
				that.images[41+3*i+j].onload = on_loaded();
				that.images[41+3*i+j].src = IMAGE_DIR+"doors_"+j+"-"+i+".png";
			}
		}

		for(let i = 0; i < 13; i++){// From 59 to 110 player (berti)
			for(let j = 0; j < 4; j++){// Reversed order for ease of access
				that.images[59+4*i+j] = new Image();
				that.images[59+4*i+j].onload = on_loaded();
				that.images[59+4*i+j].src = IMAGE_DIR+"player_"+j+"-"+i+".png";
			}
		}

		for(let i = 0; i < 9; i++){// From 111 to 146 monster 1 (purple)
			for(let j = 0; j < 4; j++){// Reversed order for ease of access
				that.images[111+4*i+j] = new Image();
				that.images[111+4*i+j].onload = on_loaded();
				that.images[111+4*i+j].src = IMAGE_DIR+"monster1_"+j+"-"+i+".png";
			}
		}

		for(let i = 0; i < 5; i++){// From 147 to 166 monster 2 (green)
			for(let j = 0; j < 4; j++){// Reversed order for ease of access
				that.images[147+4*i+j] = new Image();
				that.images[147+4*i+j].onload = on_loaded();
				that.images[147+4*i+j].src = IMAGE_DIR+"monster2_"+j+"-"+i+".png";
			}
		}

		that.images[167] = new Image();
		that.images[167].onload = on_loaded();
		that.images[167].src = IMAGE_DIR+"argl.png";

		that.images[168] = new Image();
		that.images[168].onload = on_loaded();
		that.images[168].src = IMAGE_DIR+"wow.png";

		that.images[169] = new Image();
		that.images[169].onload = on_loaded();
		that.images[169].src = IMAGE_DIR+"yeah.png";

		that.images[170] = new Image();
		that.images[170].onload = on_loaded();
		that.images[170].src = IMAGE_DIR+"exit.png";
		
		that.images[171] = new Image();
		that.images[171].onload = on_loaded();
		that.images[171].src = IMAGE_DIR+"check_b.png";
		
		that.images[172] = new Image();
		that.images[172].onload = on_loaded();
		that.images[172].src = IMAGE_DIR+"check_w.png";
		
		that.images[173] = new Image();
		that.images[173].onload = on_loaded();
		that.images[173].src = IMAGE_DIR+"dbx_confirm.png";
		
		that.images[174] = new Image();
		that.images[174].onload = on_loaded();
		that.images[174].src = IMAGE_DIR+"dbx_saveload.png";
		
		that.images[175] = new Image();
		that.images[175].onload = on_loaded();
		that.images[175].src = IMAGE_DIR+"dbx_loadlvl.png";
		
		that.images[176] = new Image();
		that.images[176].onload = on_loaded();
		that.images[176].src = IMAGE_DIR+"dbx_charts.png";
		
		that.images[177] = new Image();
		that.images[177].onload = on_loaded();
		that.images[177].src = IMAGE_DIR+"btn_c-up.png";
		
		that.images[178] = new Image();
		that.images[178].onload = on_loaded();
		that.images[178].src = IMAGE_DIR+"btn_c-down.png";
		
		that.images[179] = new Image();
		that.images[179].onload = on_loaded();
		that.images[179].src = IMAGE_DIR+"btn_n-up.png";
		
		that.images[180] = new Image();
		that.images[180].onload = on_loaded();
		that.images[180].src = IMAGE_DIR+"btn_n-down.png";
		
		that.images[181] = new Image();
		that.images[181].onload = on_loaded();
		that.images[181].src = IMAGE_DIR+"btn_o-up.png";

		that.images[182] = new Image();
		that.images[182].onload = on_loaded();
		that.images[182].src = IMAGE_DIR+"btn_o-down.png";
		
		that.images[183] = new Image();
		that.images[183].onload = on_loaded();
		that.images[183].src = IMAGE_DIR+"btn_y-up.png";
		
		that.images[184] = new Image();
		that.images[184].onload = on_loaded();
		that.images[184].src = IMAGE_DIR+"btn_y-down.png";
		
		////////////////////////////////////////////////////////
		// Sounds: /////////////////////////////////////////////
		////////////////////////////////////////////////////////
		
		let soundarray = [
		"about.mp3",
		"argl.mp3",
		"attack1.mp3",
		"attack2.mp3",
		"chart.mp3",
		"click.mp3",
		"gameend.mp3",
		"getpoint.mp3",
		"newplane.mp3",
		"opendoor.mp3",
		"wow.mp3",
		"yeah.mp3"];
		
		for(let i = 0; i < soundarray.length; i++){
			that.sounds[i] = new Audio();
			that.sounds[i].oncanplaythrough = on_loaded();
			that.sounds[i].src = SOUND_DIR+soundarray[i];
		}

		////////////////////////////////////////////////////////
		// Level: //////////////////////////////////////////////
		////////////////////////////////////////////////////////

		// levels is now loaded externally
		if(that.levels !== null){
			on_loaded();
		}
	}
}

/*//////////////////////////////////////////////////////////////////////////////////////////////////////
// VISUAL CLASS
// Everything in here is related to graphical output. Also, menus and dialog boxes
//////////////////////////////////////////////////////////////////////////////////////////////////////*/

function CLASS_visual(){
	let that = this;

	this.berti_blink_time = 0;
	this.last_rendered = 0;
	this.last_fps_update = 0;
	this.static_ups = 0;
	this.static_fps = 0;
	
	this.buttons_pressed = new Array();
	this.buttons_pressed[0] = this.buttons_pressed[1] = this.buttons_pressed[2] = false;
	
	// Animations:
	this.offset_key_x = 3;
	this.offset_key_y = 4;
	this.offset_banana_x = 4;
	this.offset_banana_y = 4;
	
	this.offset_wow_x = -20;
	this.offset_wow_y = -44;
	
	this.offset_yeah_x = -20;
	this.offset_yeah_y = -44;
	
	this.offset_argl_x = -20;
	this.offset_argl_y = -44;
	
	this.init_animation = function(){
		for(let y = 0; y < LEV_DIMENSION_Y; y++){
			for(let x = 0; x < LEV_DIMENSION_X; x++){
				let block = game.level_array[x][y];
				switch (block.id) {
					case ENT_DUMMY:
						break;
					case ENT_PLAYER_BERTI:
					case ENT_AUTO_BERTI:
						block.animation_frame = IMG_BERTI_IDLE;
						break;
					case ENT_PINNED_BLOCK:
						block.animation_frame = IMG_BLOCK_PINNED;
						break;
					case ENT_BANANA_PEEL:
						block.animation_frame = IMG_BANANA_PEEL;
						block.fine_offset_x = that.offset_banana_x;
						block.fine_offset_y = that.offset_banana_y;
						break;
					case ENT_LIGHT_BLOCK:
						block.animation_frame = IMG_BLOCK_LIGHT;
						break;
					case ENT_HEAVY_BLOCK:
						block.animation_frame = IMG_BLOCK_HEAVY;
						break;
					case ENT_PURPLE_MONSTER:
						block.animation_frame = IMG_PURPMON_STUCK_0;
						break;
					case ENT_GREEN_MONSTER:
						block.animation_frame = IMG_GREENMON_STUCK_0;
						break;
					case ENT_KEY_1:
						block.animation_frame = IMG_KEY_1;
						block.fine_offset_x = that.offset_key_x;
						block.fine_offset_y = that.offset_key_y;
						break;
					case ENT_KEY_2:
						block.animation_frame = IMG_KEY_2;
						block.fine_offset_x = that.offset_key_x;
						block.fine_offset_y = that.offset_key_y;
						break;
					case ENT_KEY_3:
						block.animation_frame = IMG_KEY_3;
						block.fine_offset_x = that.offset_key_x;
						block.fine_offset_y = that.offset_key_y;
						break;
					case ENT_KEY_4:
						block.animation_frame = IMG_KEY_4;
						block.fine_offset_x = that.offset_key_x;
						block.fine_offset_y = that.offset_key_y;
						break;
					case ENT_KEY_5:
						block.animation_frame = IMG_KEY_5;
						block.fine_offset_x = that.offset_key_x;
						block.fine_offset_y = that.offset_key_y;
						break;
					case ENT_KEY_6:
						block.animation_frame = IMG_KEY_6;
						block.fine_offset_x = that.offset_key_x;
						block.fine_offset_y = that.offset_key_y;
						break;
					case ENT_DOOR_1:
						block.animation_frame = IMG_DOOR_1_CLOSED;
						break;
					case ENT_DOOR_2:
						block.animation_frame = IMG_DOOR_2_CLOSED;
						break;
					case ENT_DOOR_3:
						block.animation_frame = IMG_DOOR_3_CLOSED;
						break;
					case ENT_DOOR_4:
						block.animation_frame = IMG_DOOR_4_CLOSED;
						break;
					case ENT_DOOR_5:
						block.animation_frame = IMG_DOOR_5_CLOSED;
						break;
					case ENT_DOOR_6:
						block.animation_frame = IMG_DOOR_6_CLOSED;
						break;
				
					default:
						// Uh oh, this part should never be executed
						break;
				}
			}
		}
	}
	
	this.update_animation = function(x, y){
		let block = game.level_array[x][y];
		switch (block.id) {
			case ENT_PLAYER_BERTI:
			case ENT_AUTO_BERTI:
				block.fine_offset_x = 0;
				if(game.level_ended == 0){
					if(block.moving){
						block.fine_offset_x = -1;
						if(block.pushing){
							switch (block.face_dir) {
								case DIR_UP:
									if(block.animation_frame < IMG_BERTI_PUSH_UP_0 || block.animation_frame > IMG_BERTI_PUSH_UP_3){
										block.animation_frame = IMG_BERTI_PUSH_UP_0;
									}
									break;
								case DIR_DOWN:
									if(block.animation_frame < IMG_BERTI_PUSH_DOWN_0 || block.animation_frame > IMG_BERTI_PUSH_DOWN_3){
										block.animation_frame = IMG_BERTI_PUSH_DOWN_0;
									}
									break;
								case DIR_LEFT:
									if(block.animation_frame < IMG_BERTI_PUSH_LEFT_0 || block.animation_frame > IMG_BERTI_PUSH_LEFT_3){
										block.animation_frame = IMG_BERTI_PUSH_LEFT_0;
									}
									break;
								case DIR_RIGHT:
									if(block.animation_frame < IMG_BERTI_PUSH_RIGHT_0 || block.animation_frame > IMG_BERTI_PUSH_RIGHT_3){
										block.animation_frame = IMG_BERTI_PUSH_RIGHT_0;
									}
									break;
								default:
									// This should never be executed
									break;
							}
						}else{
							switch (block.face_dir) {
								case DIR_UP:
									if(block.animation_frame < IMG_BERTI_WALK_UP_0 || block.animation_frame > IMG_BERTI_WALK_UP_3){
										block.animation_frame = IMG_BERTI_WALK_UP_0;
									}
									break;
								case DIR_DOWN:
									if(block.animation_frame < IMG_BERTI_WALK_DOWN_0 || block.animation_frame > IMG_BERTI_WALK_DOWN_3){
										block.animation_frame = IMG_BERTI_WALK_DOWN_0;
									}
									break;
								case DIR_LEFT:
									if(block.animation_frame < IMG_BERTI_WALK_LEFT_0 || block.animation_frame > IMG_BERTI_WALK_LEFT_3){
										block.animation_frame = IMG_BERTI_WALK_LEFT_0;
									}
									break;
								case DIR_RIGHT:
									if(block.animation_frame < IMG_BERTI_WALK_RIGHT_0 || block.animation_frame > IMG_BERTI_WALK_RIGHT_3){
										block.animation_frame = IMG_BERTI_WALK_RIGHT_0;
									}
									break;
								default:
									// This should never be executed
									break;
							}
						}
					}else{
						block.animation_frame = IMG_BERTI_IDLE;
					}
				}else if(game.level_ended == 1){
					block.animation_frame = IMG_BERTI_CELEBRATING;
				}else if(game.level_ended == 2){
					block.animation_frame = IMG_BERTI_DEAD;
				}
				break;
			case ENT_PURPLE_MONSTER:
				block.fine_offset_x = 0;
				if(game.level_ended == 0){
					if(block.moving){
						block.fine_offset_x = -1;
						if(block.pushing){
							switch (block.face_dir) {
								case DIR_UP:
									if(block.animation_frame < IMG_PURPMON_PUSH_UP_0 || block.animation_frame > IMG_PURPMON_PUSH_UP_3){
										block.animation_frame = IMG_PURPMON_PUSH_UP_0;
									}
									break;
								case DIR_DOWN:
									if(block.animation_frame < IMG_PURPMON_PUSH_DOWN_0 || block.animation_frame > IMG_PURPMON_PUSH_DOWN_3){
										block.animation_frame = IMG_PURPMON_PUSH_DOWN_0;
									}
									break;
								case DIR_LEFT:
									if(block.animation_frame < IMG_PURPMON_PUSH_LEFT_0 || block.animation_frame > IMG_PURPMON_PUSH_LEFT_3){
										block.animation_frame = IMG_PURPMON_PUSH_LEFT_0;
									}
									break;
								case DIR_RIGHT:
									if(block.animation_frame < IMG_PURPMON_PUSH_RIGHT_0 || block.animation_frame > IMG_PURPMON_PUSH_RIGHT_3){
										block.animation_frame = IMG_PURPMON_PUSH_RIGHT_0;
									}
									break;
								default:
									// This should never be executed
									break;
							}
						}else{
							switch (block.face_dir) {
								case DIR_UP:
									if(block.animation_frame < IMG_PURPMON_WALK_UP_0 || block.animation_frame > IMG_PURPMON_WALK_UP_3){
										block.animation_frame = IMG_PURPMON_WALK_UP_0;
									}
									break;
								case DIR_DOWN:
									if(block.animation_frame < IMG_PURPMON_WALK_DOWN_0 || block.animation_frame > IMG_PURPMON_WALK_DOWN_3){
										block.animation_frame = IMG_PURPMON_WALK_DOWN_0;
									}
									break;
								case DIR_LEFT:
									if(block.animation_frame < IMG_PURPMON_WALK_LEFT_0 || block.animation_frame > IMG_PURPMON_WALK_LEFT_3){
										block.animation_frame = IMG_PURPMON_WALK_LEFT_0;
									}
									break;
								case DIR_RIGHT:
									if(block.animation_frame < IMG_PURPMON_WALK_RIGHT_0 || block.animation_frame > IMG_PURPMON_WALK_RIGHT_3){
										block.animation_frame = IMG_PURPMON_WALK_RIGHT_0;
									}
									break;
								default:
									// This should never be executed
									break;
							}
						}
					}else{
						block.animation_frame = IMG_PURPMON_STUCK_0;
					}
				}else{
					block.animation_frame = IMG_PURPMON_STUCK_0;
				}
				break;
			case ENT_GREEN_MONSTER:
				block.fine_offset_x = 0;
				if(game.level_ended == 0){
					if(block.moving){
						block.fine_offset_x = -1;
						switch (block.face_dir) {
							case DIR_UP:
								if(block.animation_frame < IMG_GREENMON_WALK_UP_0 || block.animation_frame > IMG_GREENMON_WALK_UP_3){
									block.animation_frame = IMG_GREENMON_WALK_UP_0;
								}
								break;
							case DIR_DOWN:
								if(block.animation_frame < IMG_GREENMON_WALK_DOWN_0 || block.animation_frame > IMG_GREENMON_WALK_DOWN_3){
									block.animation_frame = IMG_GREENMON_WALK_DOWN_0;
								}
								break;
							case DIR_LEFT:
								if(block.animation_frame < IMG_GREENMON_WALK_LEFT_0 || block.animation_frame > IMG_GREENMON_WALK_LEFT_3){
									block.animation_frame = IMG_GREENMON_WALK_LEFT_0;
								}
								break;
							case DIR_RIGHT:
								if(block.animation_frame < IMG_GREENMON_WALK_RIGHT_0 || block.animation_frame > IMG_GREENMON_WALK_RIGHT_3){
									block.animation_frame = IMG_GREENMON_WALK_RIGHT_0;
								}
								break;
							default:
								// This should never be executed
								break;
						}
					}else{
						block.animation_frame = IMG_GREENMON_STUCK_0;
					}
				}else{
					block.animation_frame = IMG_GREENMON_STUCK_0;
				}
				break;
			case ENT_DOOR_1:
				if(block.gets_removed_in >= 0){
					block.animation_frame = IMG_DOOR_1_FADING-Math.floor(block.gets_removed_in/game.door_removal_delay*2);
				}
				break;
			case ENT_DOOR_2:
				if(block.gets_removed_in >= 0){
					block.animation_frame = IMG_DOOR_2_FADING-Math.floor(block.gets_removed_in/game.door_removal_delay*2);
				}
				break;
			case ENT_DOOR_3:
				if(block.gets_removed_in >= 0){
					block.animation_frame = IMG_DOOR_3_FADING-Math.floor(block.gets_removed_in/game.door_removal_delay*2);
				}
				break;
			case ENT_DOOR_4:
				if(block.gets_removed_in >= 0){
					block.animation_frame = IMG_DOOR_4_FADING-Math.floor(block.gets_removed_in/game.door_removal_delay*2);
				}
				break;
			case ENT_DOOR_5:
				if(block.gets_removed_in >= 0){
					block.animation_frame = IMG_DOOR_5_FADING-Math.floor(block.gets_removed_in/game.door_removal_delay*2);
				}
				break;
			case ENT_DOOR_6:
				if(block.gets_removed_in >= 0){
					block.animation_frame = IMG_DOOR_6_FADING-Math.floor(block.gets_removed_in/game.door_removal_delay*2);
				}
				break;
			default:
			break;
		}
	}
	
	this.update_all_animations = function(){
		for(let y = 0; y < LEV_DIMENSION_Y; y++){
			for(let x = 0; x < LEV_DIMENSION_X; x++){
				that.update_animation(x, y);
			}
		}
	}
	
	// Volume bar:
	this.vol_bar = new CLASS_vol_bar();
	
	function CLASS_vol_bar(){
		this.offset_x = 400;
		this.offset_y = 2;
		this.height = 17;
		this.width = 100;
		this.volume = DEFAULT_VOLUME;
		
		this.colour_1 = {r:0, g:255, b: 0};// Low volume colour: Green
		this.colour_2 = {r:255, g:0, b: 0};// High volume colour: Red
		this.colour_3 = {r:255, g:255, b: 255};// Rest of the volume bar: White
		this.colour_4 = {r:0, g:0, b: 0};// Inbetween bars: Black
		
		this.colour_5 = {r:50, g:50, b:50};// "off" colour, some grey...
	}
	
	
	// Menu stuff:
	this.black = {r:0, g:0, b: 0};
	this.dark_grey = {r:64, g:64, b:64};
	this.med_grey = {r:128, g:128, b:128};
	this.light_grey = {r:212, g:208, b:200};
	this.white = {r:255, g:255, b: 255};
	this.blue = {r:10, g:36, b:106};
	
	function CLASS_menu(a_offset_x, a_offset_y, a_height, a_submenu_list){
		this.offset_x = a_offset_x;
		this.offset_y = a_offset_y;
		this.height = a_height;
		this.width = 0;
		this.submenu_open = -1;
		
		for(let i = 0; i < a_submenu_list.length; i++){
			this.width += a_submenu_list[i].width
		}
		
		this.submenu_list = a_submenu_list;
	}
	
	function CLASS_submenu(a_width, a_dd_width, a_name, a_arr_options){
		this.width = a_width;
		this.offset_line = 9;
		this.offset_text = 17;
		
		this.dd_width = a_dd_width;
		this.dd_height = 6;
		for(let i = 0; i < a_arr_options.length; i++){
			if(a_arr_options[i].line){
				this.dd_height += this.offset_line;
			}else{
				this.dd_height += this.offset_text;
			}
		}
		
		this.name = a_name;
		this.options = a_arr_options;
	}
	
	this.menu1;

	this.init_menus = function(){
		let tautology = function(){return true;};
	
		let arr_options1 = [
		{line:false, check:0, name:"New", hotkey:"F2", effect_id:0, on:tautology},
		{line:false, check:0, name:"Load Game...", hotkey:"", effect_id:1, on:function(){return HAS_STORAGE;}},
		{line:false, check:0, name:"Save", hotkey:"", effect_id:2, on:function(){return (game.savegame.progressed && HAS_STORAGE);}},
		{line:false, check:1, name:"Pause", hotkey:"", effect_id:3, on:tautology}
		];
		
		let arr_options2 = [
		{line:false, check:1, name:"Single steps", hotkey:"F5", effect_id:4, on:tautology},
		{line:false, check:1, name:"Sound", hotkey:"", effect_id:5, on:tautology},
		{line:true, check:0, name:"", hotkey:"", effect_id:-1, on:tautology},
		{line:false, check:0, name:"Load Level", hotkey:"", effect_id:6, on:function(){return HAS_STORAGE;}},
		{line:false, check:0, name:"Change Password", hotkey:"", effect_id:7, on:function(){return (game.savegame.username !== null && HAS_STORAGE);}},
		{line:true, check:0, name:"", hotkey:"", effect_id:-1, on:tautology},
		{line:false, check:0, name:"Charts", hotkey:"", effect_id:8, on:function(){return HAS_STORAGE;}}
		];
		
		let sub_m1 = new CLASS_submenu(43, 100, "Game", arr_options1);
		let sub_m2 = new CLASS_submenu(55, 150, "Options", arr_options2);
		
		that.menu1 = new CLASS_menu(1, 2, 17, [sub_m1, sub_m2]);
	}
	
	// Dialog box stuff:
	
	function add_button(img_up, img_down, pos_x, pos_y, click_effect){
		let btn = document.createElement("img");
		btn.src = res.images[img_up].src;
		btn.style.position = "absolute";
		btn.style.width = res.images[img_up].width+"px";
		btn.style.height = res.images[img_up].height+"px";
		btn.style.left = pos_x+"px";
		btn.style.top = pos_y+"px";
		
		btn.pressed = false;
		btn.onmousedown = function(evt){btn.src = res.images[img_down].src; btn.pressed = true; evt.preventDefault();};
		btn.onmouseup = function(evt){btn.src = res.images[img_up].src; btn.pressed = false;};
		btn.onmouseout = function(evt){btn.src = res.images[img_up].src;};
		btn.onmouseover = function(evt){if(btn.pressed && input.mouse_down) btn.src = res.images[img_down].src;};
		btn.onclick = click_effect;
		
		that.dbx.appendChild(btn);
		that.dbx.arr_btn[that.dbx.arr_btn.length] = btn;
	}
	
	function add_text(text, pos_x, pos_y){
		let txt = document.createElement("p");
		txt.innerHTML = text;
		txt.style.position = "absolute";
		txt.style.left = pos_x+"px";
		txt.style.top = pos_y+"px";
		txt.style.fontFamily = "Tahoma";
		txt.style.fontSize = "12px";
		that.dbx.appendChild(txt);
	}
	
	function add_number(a_num, pos_x, pos_y, width, height){
		let num = document.createElement("p");
		num.innerHTML = a_num;
		num.style.position = "absolute";
		num.style.left = pos_x+"px";
		num.style.top = pos_y+"px";
		num.style.width = width+"px";
		num.style.height = height+"px";
		num.style.fontFamily = "Tahoma";
		num.style.fontSize = "12px";
		num.style.textAlign = "right";
		that.dbx.appendChild(num);
	}
	
	function add_title(text){
		let txt = document.createElement("p");
		txt.innerHTML = text;
		txt.style.position = "absolute";
		txt.style.left = "5px";
		txt.style.top = "-13px";
		txt.style.fontFamily = "Tahoma";
		txt.style.fontSize = "14px";
		txt.style.color = "white";
		txt.style.fontWeight = "bold";
		that.dbx.appendChild(txt);
	}
	
	function add_input(pos_x, pos_y, width, height, type){
		let txt = document.createElement("input");
		//txt.innerHTML = text;
		txt.type = type;
		txt.style.position = "absolute";
		txt.style.left = pos_x+"px";
		pos_y += 10;// Because of padding
		txt.style.top = pos_y+"px";
		txt.style.width = width+"px";
		txt.style.height = height+"px";
		txt.style.fontFamily = "Tahoma";
		txt.style.fontSize = "12px";
		
		that.dbx.appendChild(txt);
		that.dbx.arr_input[that.dbx.arr_input.length] = txt;
		
		//window.setTimeout( function() {txt.focus();}, 10);
	}
	
	function add_lvlselect(pos_x, pos_y, width, height){
		let select = document.createElement("select");
		select.size = 2;
		
		select.innerHTML = "";
		for(let i = 1; i < game.savegame.reached_level; i++){
			select.innerHTML += "<option value=\""+i+"\">\n"+i+", "+game.savegame.arr_steps[i]+"</option>";
		}
		if(game.savegame.reached_level <= 50){
			select.innerHTML += "<option value=\""+game.savegame.reached_level+"\">\n"+game.savegame.reached_level+", -</option>";
		}
		
		
		select.style.position = "absolute";
		select.style.left = pos_x+"px";
		select.style.top = pos_y+"px";
		select.style.width = width+"px";
		select.style.height = height+"px";
		select.style.fontFamily = "Tahoma";
		select.style.fontSize = "12px";
		
		that.dbx.appendChild(select);
		that.dbx.lvlselect = select;
	}
	
	function add_errfield(pos_x, pos_y){
		let ef = document.createElement("p");
		ef.innerHTML = "";
		ef.style.position = "absolute";
		ef.style.left = pos_x+"px";
		ef.style.top = pos_y+"px";
		ef.style.fontFamily = "Tahoma";
		ef.style.fontSize = "12px";
		ef.style.color = "#FF0000";
		that.dbx.appendChild(ef);
		
		that.dbx.errfield = ef;
	}
	
	this.dbx = document.createElement("div");
	this.dbx.style.position = "fixed";
	this.dbx.style.zIndex = 100;
	this.dbx.style.display = "none";
	document.body.appendChild(this.dbx);
	
	this.dbx.drag_pos = {x:0, y:0};
	this.dbx.drag = false;
	this.dbx.arr_btn = new Array();
	this.dbx.arr_input = new Array();
	this.dbx.lvlselect = null;
	this.dbx.errfield = null;
	
	this.dbx.enterfun = null;
	this.dbx.cancelfun = null;
	
	this.error_dbx = function(errno){
		if(that.dbx.errfield === null) return;
		let err_string = "";
		switch(errno){
			case ERR_EXISTS:
				err_string = "Error - the account already exists.";
				break;
			case ERR_NOSAVE:
				err_string = "Error - there are no savegames to load!";
				break;
			case ERR_WRONGPW:
				err_string = "Error - you used the wrong password.";
				break;
			case ERR_NOTFOUND:
				err_string = "Error - this username couldn't be found.";
				break;
			case ERR_EMPTYNAME:
				err_string = "Error - please fill in your name.";
				break;
			default:
				err_string = "Unknown error";
				break;
		}
		that.dbx.errfield.innerHTML = err_string;
	}
	
	this.open_dbx = function(dbx_id, opt){
		that.close_dbx();
		opt = (typeof opt !== 'undefined') ? opt : 0;
	
		switch(dbx_id){
			case DBX_CONFIRM:
			{
				add_title("Confirm");
			
				that.dbx.style.width = "256px";
				that.dbx.style.height = "154px";
				that.dbx.style.left = Math.max(Math.floor(window.innerWidth-256)/2, 0)+"px";
				that.dbx.style.top = Math.max(Math.floor(window.innerHeight-154)/2, 0)+"px";
				that.dbx.style.background = 'url('+res.images[IMG_DIALOGBOX_CONFIRM].src+')';
				
				let f_y;
				let f_n;
				let f_c = function(){that.close_dbx();};
				
				if(opt == 0){// "New Game"
					f_y = function(){that.open_dbx(DBX_SAVE, 1);};
					f_n = function(){game.clear_savegame();that.close_dbx();};
				}else if(opt == 1){// "Load Game" 
					f_y = function(){that.open_dbx(DBX_SAVE, 2);};
					f_n = function(){that.open_dbx(DBX_LOAD);};
				}
				
				that.dbx.enterfun = f_y;
				that.dbx.cancelfun = f_c;
				
				add_button(IMG_BTN_YES_UP, IMG_BTN_YES_DOWN, 20, 100, f_y);
				add_button(IMG_BTN_NO_UP, IMG_BTN_NO_DOWN, 100, 100, f_n);
				add_button(IMG_BTN_CANCEL_UP, IMG_BTN_CANCEL_DOWN, 180, 100, f_c);
				
				add_text("Do you want to save the game?", 40, 35);
				break;
			}
			case DBX_SAVE:
			{
				add_title("Save game");
			
				that.dbx.style.width = "256px";
				that.dbx.style.height = "213px";
				that.dbx.style.left = Math.max(Math.floor(window.innerWidth-256)/2, 0)+"px";
				that.dbx.style.top = Math.max(Math.floor(window.innerHeight-213)/2, 0)+"px";
				that.dbx.style.background = 'url('+res.images[IMG_DIALOGBOX_SAVELOAD].src+')';
				
				add_text("Player name:", 20, 35);
				add_input(100, 35, 120, 15, "text");
				add_text("Password:", 20, 60);
				add_input(100, 60, 120, 15, "password");
				
				let f_o;
				let f_c;
				
				if(opt == 0){// "Save game"
					f_o = function(){if(game.dbxcall_save(that.dbx.arr_input[0].value, that.dbx.arr_input[1].value)){that.close_dbx();}};
					f_c = function(){that.close_dbx();};
				}else if(opt == 1){// "New Game" -> yes, save 
					f_o = function(){if(game.dbxcall_save(that.dbx.arr_input[0].value, that.dbx.arr_input[1].value)){game.clear_savegame();that.close_dbx();}};
					f_c = function(){game.clear_savegame();that.close_dbx();};
				}else if(opt == 2){// "Load Game" -> yes, save
					f_o = function(){if(game.dbxcall_save(that.dbx.arr_input[0].value, that.dbx.arr_input[1].value)){that.open_dbx(DBX_LOAD);}};
					f_c = function(){that.open_dbx(DBX_LOAD);};
				}
				
				that.dbx.enterfun = f_o;
				that.dbx.cancelfun = f_c;
				
				add_button(IMG_BTN_OK_UP, IMG_BTN_OK_DOWN, 40, 160, f_o);
				add_button(IMG_BTN_CANCEL_UP, IMG_BTN_CANCEL_DOWN, 160, 160, f_c);
				
				add_errfield(20, 85);
				break;
			}
			case DBX_LOAD:
			{
				add_title("Load game");
			
				that.dbx.style.width = "256px";
				that.dbx.style.height = "213px";
				that.dbx.style.left = Math.max(Math.floor(window.innerWidth-256)/2, 0)+"px";
				that.dbx.style.top = Math.max(Math.floor(window.innerHeight-213)/2, 0)+"px";
				that.dbx.style.background = 'url('+res.images[IMG_DIALOGBOX_SAVELOAD].src+')';
				
				add_text("Player name:", 20, 35);
				add_input(100, 35, 120, 15, "text");
				add_text("Password:", 20, 60);
				add_input(100, 60, 120, 15, "password");
				
				let f_o = function(){if(game.dbxcall_load(that.dbx.arr_input[0].value, that.dbx.arr_input[1].value)){that.close_dbx();}};
				let f_c = function(){that.close_dbx();};
				
				that.dbx.enterfun = f_o;
				that.dbx.cancelfun = f_c;
				
				add_button(IMG_BTN_OK_UP, IMG_BTN_OK_DOWN, 40, 160, f_o);
				add_button(IMG_BTN_CANCEL_UP, IMG_BTN_CANCEL_DOWN, 160, 160, f_c);
				
				add_errfield(20, 85);
				break;
			}
			case DBX_CHPASS:
			{
				add_title("Change password");
			
				that.dbx.style.width = "256px";
				that.dbx.style.height = "213px";
				that.dbx.style.left = Math.max(Math.floor(window.innerWidth-256)/2, 0)+"px";
				that.dbx.style.top = Math.max(Math.floor(window.innerHeight-213)/2, 0)+"px";
				that.dbx.style.background = 'url('+res.images[IMG_DIALOGBOX_SAVELOAD].src+')';
				
				add_text("Old password:", 20, 35);
				add_input(100, 35, 120, 15, "password");
				add_text("New password:", 20, 60);
				add_input(100, 60, 120, 15, "password");
				
				let f_o = function(){if(game.dbxcall_chpass(that.dbx.arr_input[0].value, that.dbx.arr_input[1].value)){that.close_dbx();}};
				let f_c = function(){that.close_dbx();};
				
				that.dbx.enterfun = f_o;
				that.dbx.cancelfun = f_c;
				
				add_button(IMG_BTN_OK_UP, IMG_BTN_OK_DOWN, 40, 160, f_o);
				add_button(IMG_BTN_CANCEL_UP, IMG_BTN_CANCEL_DOWN, 160, 160, f_c);
				
				add_errfield(20, 85);
				break;
			}
			case DBX_LOADLVL:
			{
				add_title("Load level");
			
				that.dbx.style.width = "197px";
				that.dbx.style.height = "273px";
				that.dbx.style.left = Math.max(Math.floor(window.innerWidth-197)/2, 0)+"px";
				that.dbx.style.top = Math.max(Math.floor(window.innerHeight-273)/2, 0)+"px";
				that.dbx.style.background = 'url('+res.images[IMG_DIALOGBOX_LOADLVL].src+')';
				
				add_lvlselect(20, 80, 158, 109);
				
				let f_o = function(){if(parseInt(that.dbx.lvlselect.value) > 0) {game.load_level(parseInt(that.dbx.lvlselect.value)); that.close_dbx();}};
				let f_c = function(){that.close_dbx();};
				
				that.dbx.enterfun = f_o;
				that.dbx.cancelfun = f_c;
				
				add_button(IMG_BTN_OK_UP, IMG_BTN_OK_DOWN, 25, 220, f_o);
				add_button(IMG_BTN_CANCEL_UP, IMG_BTN_CANCEL_DOWN, 105, 220, f_c);
				
				add_text("Player name:", 20, 30);
				if(game.savegame.username === null){
					add_text("- none -", 100, 30);
				}else{
					add_text(game.savegame.username, 100, 30);
				}
				
				add_text("Level, steps:", 20, 50);
				
				break;
			}
			case DBX_CHARTS:
			{
				game.play_sound(4);
				
				add_title("Charts");
				
				that.dbx.style.width = "322px";
				that.dbx.style.height = "346px";
				that.dbx.style.left = Math.max(Math.floor(window.innerWidth-322)/2, 0)+"px";
				that.dbx.style.top = Math.max(Math.floor(window.innerHeight-346)/2, 0)+"px";
				that.dbx.style.background = 'url('+res.images[IMG_DIALOGBOX_CHARTS].src+')';
				
				let uc = localStorage.getItem("user_count");
				let user_arr = new Array();
				
				for(let i = 0; i < uc; i++){
					let prefix = "player"+i+"_";
					let rl = parseInt(localStorage.getItem(prefix+"reached_level"));
					let st = 0;
					for(let j = 1; j < rl; j++){
						st += parseInt(localStorage.getItem(prefix+"steps_lv"+j));
					}
					user_arr[i] = {name: localStorage.getItem(prefix+"username"), reached: rl, steps: st}
				}
				
				user_arr.sort(function(a,b){return (b.reached-a.reached == 0)?(a.steps - b.steps):(b.reached-a.reached);});
				
				add_text("rank", 21, 37);
				add_text("level", 57, 37);
				add_text("steps", 100, 37);
				add_text("name", 150, 37);
				
				for(let i = 0; i < uc && i < 10; i++){
					add_number((i+1), 20, 65+18*i, 20, 20);
					add_number(user_arr[i].reached, 50, 65+18*i, 30, 20);
					add_number(user_arr[i].steps, 95, 65+18*i, 40, 20);
					add_text(user_arr[i].name, 155, 65+18*i);
				}
				
				let f_o = function(){that.close_dbx();};
				
				that.dbx.enterfun = f_o;
				that.dbx.cancelfun = f_o;
				
				add_button(IMG_BTN_OK_UP, IMG_BTN_OK_DOWN, 125, 300, f_o);
				break;
			}
			default:
				break;
		}
		that.dbx.style.display = "inline";
		
		if(that.dbx.arr_input[0]){
			that.dbx.arr_input[0].focus();
		}
	}
	
	this.close_dbx = function(){
		that.dbx.style.display = "none";
		
		// IMPORTANT MEMORY LEAK PREVENTION
		for(let i = that.dbx.arr_btn.length-1; i >= 0; i--){
			that.dbx.arr_btn[i].pressed = null;
			that.dbx.arr_btn[i].onmousedown = null;
			that.dbx.arr_btn[i].onmouseup = null;
			that.dbx.arr_btn[i].onmouseout = null;
			that.dbx.arr_btn[i].onmouseover = null;
			that.dbx.arr_btn[i].onclick = null;
			that.dbx.arr_btn[i] = null;
		}
		that.dbx.arr_btn = new Array();
		
		for(let i = that.dbx.arr_input.length-1; i >= 0; i--){
			that.dbx.arr_input[i] = null;
		}
		that.dbx.arr_input = new Array();
		
		that.dbx.lvlselect = null;
		that.dbx.errfield = null;
		
		that.dbx.enterfun = null;
		that.dbx.cancelfun = null;
		
		while (that.dbx.firstChild) {
			that.dbx.removeChild(that.dbx.firstChild);
		}
	}
	
}

/*//////////////////////////////////////////////////////////////////////////////////////////////////////
// UPDATING PROCESS
// Here, the behaviour of the game is calculated, once per UPS (update per second)
//////////////////////////////////////////////////////////////////////////////////////////////////////*/
let update = function () {
	if(res.ready()){// All resources loaded
		if(!game.initialized){
			game.set_volume(DEFAULT_VOLUME);
			input.init();// Only init inputs after everything is loaded.
			game.play_sound(0);
			game.initialized = true;
		}
		
		if(!game.paused){
			if(game.mode == 0){
				game.wait_timer--;
				if(game.wait_timer <= 0){
					game.load_level(0);
				}
			}else if(game.mode == 1){
				if(game.wait_timer <= 0){
					if(game.level_ended == 0){
						game.update_tick++;
						update_entities();
					}else if(game.level_ended == 1){
						game.update_savegame(game.level_number, game.steps_taken);
						game.next_level();
					}else if(game.level_ended == 2){
						game.reset_level();
					}
				}else{
					game.wait_timer--;
				}
			}
		}
	}
	
	let now = Date.now();
	game.delta_updated = now - game.last_updated;
	game.last_updated = now;
	
	game.update_drawn = false;
};

let update_entities = function(){
	let tick = (game.update_tick*60/UPS);
	let synced_move = tick % (12/game.move_speed) == 0;
	
	// The player moves first at all times to ensure the best response time and remove directional quirks.
	for(let i = 0; i < game.berti_positions.length; i++){
		game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].register_input(game.berti_positions[i].x, game.berti_positions[i].y, !synced_move);
	}
	
	if(synced_move){
		// NPC logic and stop walking logic.
		for(let y = 0; y < LEV_DIMENSION_Y; y++){
			for(let x = 0; x < LEV_DIMENSION_X; x++){
				if(game.level_array[x][y].id == ENT_AUTO_BERTI){
					game.level_array[x][y].move_randomly(x,y);
				}else if(game.level_array[x][y].id == ENT_PURPLE_MONSTER || game.level_array[x][y].id == ENT_GREEN_MONSTER){
					game.level_array[x][y].chase_berti(x,y);
				}
				
				if(game.level_array[x][y].just_moved){
					game.level_array[x][y].just_moved = false;
					vis.update_animation(x,y);
				}
			}
		}
	}

	// After calculating who moves where, the entities actually get updated.
	for(let y = 0; y < LEV_DIMENSION_Y; y++){
		for(let x = 0; x < LEV_DIMENSION_X; x++){
			game.level_array[x][y].update_entity(x,y);
		}
	}
	
	// Gameover condition check.
	for(let i = 0; i < game.berti_positions.length; i++){
		game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].check_enemy_proximity(game.berti_positions[i].x, game.berti_positions[i].y);
	}
}

/*//////////////////////////////////////////////////////////////////////////////////////////////////////
// RENDERING PROCESS
// All visual things get handled here. Visual variables go into the object "vis".
// Runs with 60 FPS on average (depending on browser).
//////////////////////////////////////////////////////////////////////////////////////////////////////*/

// Render scene
let render = function () {
	let now = Date.now();
    let elapsed = now - game.then;
	
	// Fudge factor: Tolerate timing inaccuracies without skipping update step
	// Reason: Deliberate reduction in timing accuracy due to browser security
	const fudge_factor = 2;
	if (elapsed + fudge_factor > game.fpsInterval) {
		if (elapsed > game.fpsInterval) {
			game.then = now - (elapsed % game.fpsInterval);
		}else{
			game.then = now;
		}
		update();
	}
	
	//CTX.fillStyle="red";
	//CTX.fillRect(0, 0, SCREEN_WIDTH, MENU_HEIGHT);
	//CTX.clearRect(0, MENU_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT-MENU_HEIGHT);
	
	if (game.update_drawn) {// This prevents the game from rendering the same thing twice
		window.requestAnimationFrame(render);
		return;
	}
	game.update_drawn = true;

	if (res.ready()) {
		CTX.drawImage(res.images[IMG_BACKGROUND], 0, 0);
		CTX.drawImage(res.images[IMG_FOOTSTEPS], 22, 41);
		CTX.drawImage(res.images[IMG_LADDER], 427, 41);
		render_displays();
		render_buttons();
		if(game.mode == 0){// Title image
			CTX.drawImage(res.images[IMG_TITLESCREEN], LEV_OFFSET_X+4, LEV_OFFSET_Y+4);
			
			CTX.fillStyle = "rgb(0, 0, 0)";
			CTX.font = "bold 12px Helvetica";
			CTX.textAlign = "left";
			CTX.textBaseline = "bottom";
			CTX.fillText("JavaScript remake by " + AUTHOR, 140, 234);
		}else if(game.mode == 1){
			render_field();
		}else if(game.mode == 2){// Won!
			CTX.drawImage(res.images[IMG_ENDSCREEN], LEV_OFFSET_X+4, LEV_OFFSET_Y+4);
		}
		render_vol_bar();
		render_menu();
	}else{
		CTX.fillStyle = "rgb("+vis.light_grey.r+", "+vis.light_grey.g+", "+vis.light_grey.b+")";
		CTX.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);// Options box
		CTX.fillStyle = "rgb(0, 0, 0)";
		CTX.font = "36px Helvetica";
		CTX.textAlign = "center";
		CTX.textBaseline = "middle";
		CTX.fillText("Loading...", SCREEN_WIDTH/2,SCREEN_HEIGHT/2);
	}
	if(DEBUG) render_fps();
	
	window.requestAnimationFrame(render);
};

function render_fps(){
	let now = Date.now();
	
	if(now - vis.last_fps_update >= 250){
		let delta_rendered = now - vis.last_rendered;
		vis.static_ups = ((1000/game.delta_updated).toFixed(2));
		vis.static_fps = ((1000/delta_rendered).toFixed(2));
		
		vis.last_fps_update = now;
	}
	
	CTX.fillStyle = "rgb(255, 0, 0)";
	CTX.font = "12px Helvetica";
	CTX.textAlign = "right";
	CTX.textBaseline = "bottom";
	CTX.fillText("UPS: " + vis.static_ups +" FPS:" + vis.static_fps + " ", SCREEN_WIDTH,SCREEN_HEIGHT);

	vis.last_rendered = now;
};

function render_menu(){
	let submenu_offset = 0;
	// The font is the same for the whole menu... Segoe UI is also nice
	CTX.font = "11px Tahoma";
	CTX.textAlign = "left";
	CTX.textBaseline = "top";
	
	for(let i = 0; i < vis.menu1.submenu_list.length; i++){
		let sm = vis.menu1.submenu_list[i];
		if(i == vis.menu1.submenu_open){
			CTX.fillStyle = "rgb("+vis.light_grey.r+", "+vis.light_grey.g+", "+vis.light_grey.b+")";
			CTX.fillRect(vis.menu1.offset_x + submenu_offset, vis.menu1.offset_y + vis.menu1.height + 1, sm.dd_width, sm.dd_height);// Options box
		
			CTX.fillStyle = "rgb("+vis.med_grey.r+", "+vis.med_grey.g+", "+vis.med_grey.b+")";
			CTX.fillRect(vis.menu1.offset_x + submenu_offset, vis.menu1.offset_y, sm.width, 1);
			CTX.fillRect(vis.menu1.offset_x + submenu_offset, vis.menu1.offset_y, 1, vis.menu1.height);
			CTX.fillRect(vis.menu1.offset_x + submenu_offset + sm.dd_width - 2, vis.menu1.offset_y + vis.menu1.height + 2, 1, sm.dd_height - 2);// Options box
			CTX.fillRect(vis.menu1.offset_x + submenu_offset + 1, vis.menu1.offset_y + vis.menu1.height + sm.dd_height - 1, sm.dd_width - 2, 1);// Options box
			
			CTX.fillStyle = "rgb("+vis.white.r+", "+vis.white.g+", "+vis.white.b+")";
			CTX.fillRect(vis.menu1.offset_x + submenu_offset, vis.menu1.offset_y + vis.menu1.height, sm.width, 1);
			CTX.fillRect(vis.menu1.offset_x + submenu_offset + sm.width - 1, vis.menu1.offset_y, 1, vis.menu1.height);
			CTX.fillRect(vis.menu1.offset_x + submenu_offset + 1, vis.menu1.offset_y + vis.menu1.height + 2, 1, sm.dd_height - 3);// Options box
			CTX.fillRect(vis.menu1.offset_x + submenu_offset + 1, vis.menu1.offset_y + vis.menu1.height + 2, sm.dd_width - 3, 1);// Options box
			
			CTX.fillStyle = "rgb("+vis.dark_grey.r+", "+vis.dark_grey.g+", "+vis.dark_grey.b+")";
			CTX.fillRect(vis.menu1.offset_x + submenu_offset + sm.dd_width - 1, vis.menu1.offset_y + vis.menu1.height + 1, 1, sm.dd_height);// Options box
			CTX.fillRect(vis.menu1.offset_x + submenu_offset, vis.menu1.offset_y + vis.menu1.height + sm.dd_height, sm.dd_width - 1, 1);// Options box
			
			//input.mouse_pos.x
			let option_offset = vis.menu1.offset_y + vis.menu1.height + 4;
			CTX.fillStyle = "rgb("+vis.black.r+", "+vis.black.g+", "+vis.black.b+")";
			
			for(let j = 0; j < sm.options.length; j++){
				let next_offset;
				let check_image = IMG_CHECKBOX_CHECKED;
				
				if(sm.options[j].line){
					next_offset = option_offset + sm.offset_line;
					
					CTX.fillStyle = "rgb("+vis.med_grey.r+", "+vis.med_grey.g+", "+vis.med_grey.b+")";
					CTX.fillRect(vis.menu1.offset_x + submenu_offset + 3 , option_offset + 3, sm.dd_width - 6, 1);// Separator line
					CTX.fillStyle = "rgb("+vis.white.r+", "+vis.white.g+", "+vis.white.b+")";
					CTX.fillRect(vis.menu1.offset_x + submenu_offset + 3 , option_offset + 4, sm.dd_width - 6, 1);// Separator line
					
				}else{
					next_offset = option_offset + sm.offset_text;
				}
				
				if(!sm.options[j].line && input.mouse_pos.x > vis.menu1.offset_x + submenu_offset && input.mouse_pos.x < vis.menu1.offset_x + submenu_offset + sm.dd_width &&
				input.mouse_pos.y > option_offset && input.mouse_pos.y < next_offset){
					CTX.fillStyle = "rgb("+vis.blue.r+", "+vis.blue.g+", "+vis.blue.b+")";
					CTX.fillRect(vis.menu1.offset_x + submenu_offset + 3 , option_offset, sm.dd_width - 6, sm.offset_text);// Options box
					CTX.fillStyle = "rgb("+vis.white.r+", "+vis.white.g+", "+vis.white.b+")";
					
					check_image = IMG_CHECKBOX_UNCHECKED;
				}else if(!sm.options[j].on()){
					CTX.fillStyle = "rgb("+vis.white.r+", "+vis.white.g+", "+vis.white.b+")";
					CTX.fillText(sm.options[j].name, vis.menu1.offset_x + submenu_offset + 21, option_offset + 2);
				}else{
					CTX.fillStyle = "rgb("+vis.black.r+", "+vis.black.g+", "+vis.black.b+")";
				}
				
				if(sm.options[j].on()){
					CTX.fillText(sm.options[j].name, vis.menu1.offset_x + submenu_offset + 20, option_offset + 1);
				}else{
					CTX.fillStyle = "rgb("+vis.med_grey.r+", "+vis.med_grey.g+", "+vis.med_grey.b+")";
					CTX.fillText(sm.options[j].name, vis.menu1.offset_x + submenu_offset + 20, option_offset + 1);
				}
				
				if(sm.options[j].check != 0){
					if((sm.options[j].effect_id == 3 && game.paused) || (sm.options[j].effect_id == 4 && game.single_steps) || (sm.options[j].effect_id == 5 && game.sound)){
						CTX.drawImage(res.images[check_image], vis.menu1.offset_x + submenu_offset + 6, option_offset + 6);// Background
					}
				}
				
				option_offset = next_offset;
			}
			
		}
		CTX.fillStyle = "rgb("+vis.black.r+", "+vis.black.g+", "+vis.black.b+")";
		CTX.fillText(sm.name, vis.menu1.offset_x + submenu_offset + 6, vis.menu1.offset_y + 3);
		submenu_offset += sm.width;
	}
}

function render_vol_bar(){
	let vb = vis.vol_bar;
	let switcher = false;
	let line_height = 0;
	
	for(let i = 0; i < vb.width; i+= 1){
		if(switcher){
			switcher = false;
			CTX.fillStyle = "rgb("+vb.colour_4.r+", "+vb.colour_4.g+", "+vb.colour_4.b+")";
		}else{
			switcher = true;
			let ratio2 = i/vb.width;
			line_height = Math.round(vb.height*ratio2);
		
			if(i < Math.ceil(vb.volume*vb.width)){
				if(game.sound){
					let ratio1 = 1-ratio2;
					CTX.fillStyle = "rgb("+Math.round(vb.colour_1.r*ratio1+vb.colour_2.r*ratio2)+", "+Math.round(vb.colour_1.g*ratio1+vb.colour_2.g*ratio2)+", "+Math.round(vb.colour_1.b*ratio1+vb.colour_2.b*ratio2)+")";
				}else{
					CTX.fillStyle = "rgb("+vb.colour_5.r+", "+vb.colour_5.g+", "+vb.colour_5.b+")";
				}
			}else{
				CTX.fillStyle = "rgb("+vb.colour_3.r+", "+vb.colour_3.g+", "+vb.colour_3.b+")";
			}
		}
		CTX.fillRect(vb.offset_x+i, vb.offset_y+vb.height-line_height, 1, line_height);
	}

};

function render_field(){
	render_field_subset(true);// Consumables in the background
	render_field_subset(false);// The rest in the foreground
	
	CTX.drawImage(res.images[IMG_BACKGROUND], 0, 391, 537, 4, 0, LEV_OFFSET_Y+24*LEV_DIMENSION_Y, 537, 4);// Bottom border covering blocks
	CTX.drawImage(res.images[IMG_BACKGROUND], 520, LEV_OFFSET_Y, 4, 391-LEV_OFFSET_Y, LEV_OFFSET_X+24*LEV_DIMENSION_X, LEV_OFFSET_Y, 4, 391-LEV_OFFSET_Y);// Right border covering blocks
	
	if(game.level_ended == 1){// Berti cheering, wow or yeah
		for(let i = 0; i < game.berti_positions.length; i++){
			if(game.wow){
				CTX.drawImage(res.images[IMG_WOW],
				LEV_OFFSET_X+24*game.berti_positions[i].x+game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].moving_offset.x+vis.offset_wow_x,
				LEV_OFFSET_Y+24*game.berti_positions[i].y+game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].moving_offset.y+vis.offset_wow_y);
			}else{
				CTX.drawImage(res.images[IMG_YEAH],
				LEV_OFFSET_X+24*game.berti_positions[i].x+game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].moving_offset.x+vis.offset_yeah_x,
				LEV_OFFSET_Y+24*game.berti_positions[i].y+game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].moving_offset.y+vis.offset_yeah_y);
			}
		}
	}else if(game.level_ended == 2){// Berti dies in a pool of blood
		for(let i = 0; i < game.berti_positions.length; i++){
			CTX.drawImage(res.images[IMG_ARGL],
			LEV_OFFSET_X+24*game.berti_positions[i].x+game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].moving_offset.x+vis.offset_argl_x,
			LEV_OFFSET_Y+24*game.berti_positions[i].y+game.level_array[game.berti_positions[i].x][game.berti_positions[i].y].moving_offset.y+vis.offset_argl_y);
		}
	}
}
function render_field_subset(consumable){
	for(let y = 0; y < LEV_DIMENSION_Y; y++){
		for(let x = 0; x < LEV_DIMENSION_X; x++){
			let block = game.level_array[x][y];
			if(y > 0 && game.level_array[x][y-1].moving && game.level_array[x][y-1].face_dir == DIR_DOWN && game.level_array[x][y-1].consumable == consumable){
				render_block(x, y-1, RENDER_BOTTOM);
			}
			
			if(y > 0 && (!game.level_array[x][y-1].moving) && game.level_array[x][y-1].consumable == consumable){
				if(x > 0 && game.level_array[x-1][y].face_dir != DIR_RIGHT){
					render_block(x, y-1, RENDER_BOTTOM_BORDER);
				}
			}
		
			if(block.consumable == consumable){
				if(!block.moving || block.face_dir == DIR_LEFT || block.face_dir == DIR_RIGHT){
					render_block(x, y, RENDER_FULL);
				}else if(block.face_dir == DIR_DOWN){
					render_block(x, y, RENDER_TOP);
				}else if(block.face_dir == DIR_UP){
					render_block(x, y, RENDER_BOTTOM);
				}
			}
			
			if(y+1 < LEV_DIMENSION_Y && game.level_array[x][y+1].moving && game.level_array[x][y+1].face_dir == DIR_UP && game.level_array[x][y+1].consumable == consumable){
				render_block(x, y+1, RENDER_TOP);
			}
		}
	}
}
function render_block(x, y, render_option){
	let block = game.level_array[x][y];

	let offset_x = block.moving_offset.x;
	let offset_y = block.moving_offset.y;
	
	let needs_update = false;
	while(block.animation_delay >= ANIMATION_DURATION && !block.just_moved){
		block.animation_delay -= ANIMATION_DURATION;
		needs_update = true;
	}
	
	if(game.level_array[x][y].id == ENT_EMPTY || game.level_array[x][y].id == ENT_DUMMY){
		// Optimization (empty and dummy block can't be drawn)
		return;
	}
	
	if(needs_update)
	switch (game.level_array[x][y].id) {
		case ENT_PLAYER_BERTI:
		case ENT_AUTO_BERTI:
			if(block.animation_frame >= IMG_BERTI_WALK_LEFT_0 && block.animation_frame < IMG_BERTI_WALK_LEFT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_WALK_LEFT_3){
				block.animation_frame = IMG_BERTI_WALK_LEFT_0;
			}else if(block.animation_frame >= IMG_BERTI_WALK_RIGHT_0 && block.animation_frame < IMG_BERTI_WALK_RIGHT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_WALK_RIGHT_3){
				block.animation_frame = IMG_BERTI_WALK_RIGHT_0;
			}else if(block.animation_frame >= IMG_BERTI_WALK_UP_0 && block.animation_frame < IMG_BERTI_WALK_UP_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_WALK_UP_3){
				block.animation_frame = IMG_BERTI_WALK_UP_0;
			}else if(block.animation_frame >= IMG_BERTI_WALK_DOWN_0 && block.animation_frame < IMG_BERTI_WALK_DOWN_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_WALK_DOWN_3){
				block.animation_frame = IMG_BERTI_WALK_DOWN_0;
			}else if(block.animation_frame >= IMG_BERTI_PUSH_LEFT_0 && block.animation_frame < IMG_BERTI_PUSH_LEFT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_PUSH_LEFT_3){
				block.animation_frame = IMG_BERTI_PUSH_LEFT_0;
			}else if(block.animation_frame >= IMG_BERTI_PUSH_RIGHT_0 && block.animation_frame < IMG_BERTI_PUSH_RIGHT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_PUSH_RIGHT_3){
				block.animation_frame = IMG_BERTI_PUSH_RIGHT_0;
			}else if(block.animation_frame >= IMG_BERTI_PUSH_UP_0 && block.animation_frame < IMG_BERTI_PUSH_UP_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_PUSH_UP_3){
				block.animation_frame = IMG_BERTI_PUSH_UP_0;
			}else if(block.animation_frame >= IMG_BERTI_PUSH_DOWN_0 && block.animation_frame < IMG_BERTI_PUSH_DOWN_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_BERTI_PUSH_DOWN_3){
				block.animation_frame = IMG_BERTI_PUSH_DOWN_0;
			}
			break;
		case ENT_PURPLE_MONSTER:
			if(block.animation_frame >= IMG_PURPMON_STUCK_0 && block.animation_frame < IMG_PURPMON_STUCK_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_STUCK_3){
				block.animation_frame = IMG_PURPMON_STUCK_0;
			}else if(block.animation_frame >= IMG_PURPMON_WALK_LEFT_0 && block.animation_frame < IMG_PURPMON_WALK_LEFT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_WALK_LEFT_3){
				block.animation_frame = IMG_PURPMON_WALK_LEFT_0;
			}else if(block.animation_frame >= IMG_PURPMON_WALK_RIGHT_0 && block.animation_frame < IMG_PURPMON_WALK_RIGHT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_WALK_RIGHT_3){
				block.animation_frame = IMG_PURPMON_WALK_RIGHT_0;
			}else if(block.animation_frame >= IMG_PURPMON_WALK_UP_0 && block.animation_frame < IMG_PURPMON_WALK_UP_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_WALK_UP_3){
				block.animation_frame = IMG_PURPMON_WALK_UP_0;
			}else if(block.animation_frame >= IMG_PURPMON_WALK_DOWN_0 && block.animation_frame < IMG_PURPMON_WALK_DOWN_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_WALK_DOWN_3){
				block.animation_frame = IMG_PURPMON_WALK_DOWN_0;
			}else if(block.animation_frame >= IMG_PURPMON_PUSH_LEFT_0 && block.animation_frame < IMG_PURPMON_PUSH_LEFT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_PUSH_LEFT_3){
				block.animation_frame = IMG_PURPMON_PUSH_LEFT_0;
			}else if(block.animation_frame >= IMG_PURPMON_PUSH_RIGHT_0 && block.animation_frame < IMG_PURPMON_PUSH_RIGHT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_PUSH_RIGHT_3){
				block.animation_frame = IMG_PURPMON_PUSH_RIGHT_0;
			}else if(block.animation_frame >= IMG_PURPMON_PUSH_UP_0 && block.animation_frame < IMG_PURPMON_PUSH_UP_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_PUSH_UP_3){
				block.animation_frame = IMG_PURPMON_PUSH_UP_0;
			}else if(block.animation_frame >= IMG_PURPMON_PUSH_DOWN_0 && block.animation_frame < IMG_PURPMON_PUSH_DOWN_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_PURPMON_PUSH_DOWN_3){
				block.animation_frame = IMG_PURPMON_PUSH_DOWN_0;
			}
			break;
		case ENT_GREEN_MONSTER:
			if(block.animation_frame >= IMG_GREENMON_STUCK_0 && block.animation_frame < IMG_GREENMON_STUCK_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_GREENMON_STUCK_3){
				block.animation_frame = IMG_GREENMON_STUCK_0;
			}else if(block.animation_frame >= IMG_GREENMON_WALK_LEFT_0 && block.animation_frame < IMG_GREENMON_WALK_LEFT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_GREENMON_WALK_LEFT_3){
				block.animation_frame = IMG_GREENMON_WALK_LEFT_0;
			}else if(block.animation_frame >= IMG_GREENMON_WALK_RIGHT_0 && block.animation_frame < IMG_GREENMON_WALK_RIGHT_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_GREENMON_WALK_RIGHT_3){
				block.animation_frame = IMG_GREENMON_WALK_RIGHT_0;
			}else if(block.animation_frame >= IMG_GREENMON_WALK_UP_0 && block.animation_frame < IMG_GREENMON_WALK_UP_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_GREENMON_WALK_UP_3){
				block.animation_frame = IMG_GREENMON_WALK_UP_0;
			}else if(block.animation_frame >= IMG_GREENMON_WALK_DOWN_0 && block.animation_frame < IMG_GREENMON_WALK_DOWN_3){
				block.animation_frame += 1;
			}else if(block.animation_frame == IMG_GREENMON_WALK_DOWN_3){
				block.animation_frame = IMG_GREENMON_WALK_DOWN_0;
			}
			break;
		default:
		break;
	}
	
	//drawImage reference: context.drawImage(img,sx,sy,swidth,sheight,x,y,width,height);
	if(block.animation_frame >= 0){
		if(render_option == RENDER_FULL){// Render the full block
			CTX.drawImage(res.images[block.animation_frame], LEV_OFFSET_X+24*x+offset_x+block.fine_offset_x, LEV_OFFSET_Y+24*y+offset_y+block.fine_offset_y);
		}else if(render_option == RENDER_TOP){// Render top
			if(block.face_dir == DIR_DOWN){
				CTX.drawImage(res.images[block.animation_frame], 0, 0, res.images[block.animation_frame].width, res.images[block.animation_frame].height-offset_y, LEV_OFFSET_X+24*x+offset_x+block.fine_offset_x, LEV_OFFSET_Y+24*y+offset_y+block.fine_offset_y, res.images[block.animation_frame].width, res.images[block.animation_frame].height-offset_y);
			}else if(block.face_dir == DIR_UP){
				CTX.drawImage(res.images[block.animation_frame], 0, 0, res.images[block.animation_frame].width, res.images[block.animation_frame].height-offset_y-24, LEV_OFFSET_X+24*x+offset_x+block.fine_offset_x, LEV_OFFSET_Y+24*y+offset_y+block.fine_offset_y, res.images[block.animation_frame].width, res.images[block.animation_frame].height-offset_y-24);
			}
		}else if(render_option == RENDER_BOTTOM){// Render bottom
			let imgsize_offset = res.images[block.animation_frame].height - 24;
		
			if(block.face_dir == DIR_DOWN){
				CTX.drawImage(res.images[block.animation_frame], 0, res.images[block.animation_frame].height-offset_y-imgsize_offset, res.images[block.animation_frame].width, offset_y+imgsize_offset, LEV_OFFSET_X+24*x+offset_x+block.fine_offset_x, LEV_OFFSET_Y+24*y+24+block.fine_offset_y, res.images[block.animation_frame].width, offset_y+imgsize_offset);
			}else if(block.face_dir == DIR_UP){
				CTX.drawImage(res.images[block.animation_frame], 0, -offset_y, res.images[block.animation_frame].width, res.images[block.animation_frame].height+offset_y, LEV_OFFSET_X+24*x+offset_x+block.fine_offset_x, LEV_OFFSET_Y+24*y+block.fine_offset_y, res.images[block.animation_frame].width, res.images[block.animation_frame].height+offset_y);
			}
		}else if(render_option == RENDER_BOTTOM_BORDER){// Render the bottom 4 pixels
			CTX.drawImage(res.images[block.animation_frame], 0, 24, res.images[block.animation_frame].width-4, 4, LEV_OFFSET_X+24*x+offset_x+block.fine_offset_x, LEV_OFFSET_Y+24*y+offset_y+block.fine_offset_y+24, res.images[block.animation_frame].width-4, 4);
		}
	}
}

function render_buttons(){
	let over_button = false;
	if(input.mouse_down){
		if(input.mouse_pos.y >= 35 && input.mouse_pos.y <= 65){
			if(input.mouse_pos.x >= 219 && input.mouse_pos.x <= 249 && input.lastclick_button == 0){
				vis.buttons_pressed[0] = true;
				over_button = true;
			}else if(input.mouse_pos.x >= 253 && input.mouse_pos.x <= 283 && input.lastclick_button == 1){
				vis.buttons_pressed[1] = true;
				over_button = true;
			}else if(input.mouse_pos.x >= 287 && input.mouse_pos.x <= 317 && input.lastclick_button == 2){
				vis.buttons_pressed[2] = true;
				over_button = true;
			}
		}
	}
	if(!over_button){
		vis.buttons_pressed[0] = vis.buttons_pressed[1] = vis.buttons_pressed[2] = false;
	}
	
	if(game.buttons_activated[0]){
		if(vis.buttons_pressed[0]){
			CTX.drawImage(res.images[IMG_BTN_PREV_DOWN], 219, 35);// << pressed
		}else{
			CTX.drawImage(res.images[IMG_BTN_PREV_UP], 219, 35);// << up
		}
	}else{
		CTX.drawImage(res.images[IMG_BTN_PREV_DISABLED], 219, 35);// << disabled
	}
	
	if(vis.buttons_pressed[1]){
		CTX.drawImage(res.images[IMG_BTN_BERTI_DOWN], 253, 35);// Berti pressed
	}else{
		if(vis.berti_blink_time < 100){
			CTX.drawImage(res.images[IMG_BTN_BERTI_UP], 253, 35);// Berti up
			if(vis.berti_blink_time == 0){
				vis.berti_blink_time = 103;//Math.floor(100+(Math.random()*100)+1);
			}else{
				vis.berti_blink_time--;
			}
		}else{
			CTX.drawImage(res.images[IMG_BTN_BERTI_BLINK_UP], 253, 35);// Berti up blink
			if(vis.berti_blink_time == 100){
				vis.berti_blink_time = Math.floor((Math.random()*95)+5);
			}else{
				vis.berti_blink_time--;
			}
		}
	}
	
	if(game.buttons_activated[2]){
		if(vis.buttons_pressed[2]){
			CTX.drawImage(res.images[IMG_BTN_NEXT_DOWN], 287, 35);// >> pressed
		}else{
			CTX.drawImage(res.images[IMG_BTN_NEXT_UP], 287, 35);// >> up
		}
	}else{
		CTX.drawImage(res.images[IMG_BTN_NEXT_DISABLED], 287, 35);// >> disabled
	}

}

function render_displays(){
	let steps_string = game.steps_taken.toString();
	let steps_length = Math.min(steps_string.length-1, 4);

	for(let i = steps_length; i >= 0; i--){
		var img = IMG_DIGIT_LOOKUP[parseInt(steps_string.charAt(i))];
		CTX.drawImage(res.images[img], 101-(steps_length-i)*13, 41);
	}
	for(let i = steps_length+1; i < 5; i++){
		CTX.drawImage(res.images[IMG_DIGIT_EMPTY], 101-i*13, 41);
	}

	let level_string = game.level_number.toString();
	let level_length = Math.min(level_string.length-1, 4);

	for(let i = level_length; i >= 0; i--){
		var img = IMG_DIGIT_LOOKUP[parseInt(level_string.charAt(i))];
		CTX.drawImage(res.images[img], 506-(level_length-i)*13, 41);
	}
	for(let i = level_length+1; i < 5; i++){
		CTX.drawImage(res.images[IMG_DIGIT_EMPTY], 506-i*13, 41);
	}
}

function render_joystick(x, y){
	let mid_x = JOYSTICK.width/2;
	let mid_y = JOYSTICK.height/2;
	
	JOYCTX.clearRect ( 0 , 0 , JOYSTICK.width, JOYSTICK.height );
	JOYCTX.globalAlpha = 0.5;// Set joystick half-opaque (1 = opaque, 0 = fully transparent)
	JOYCTX.beginPath();
	JOYCTX.arc(mid_x,mid_y,JOYSTICK.width/4+10,0,2*Math.PI);
	JOYCTX.stroke();
	
	if(typeof x !== 'undefined' && typeof y !== 'undefined'){
		let dist = Math.sqrt(Math.pow(x-mid_x,2)+Math.pow(y-mid_y,2));
		if(dist > JOYSTICK.width/4){
			x = mid_x + (x-mid_x)/dist*JOYSTICK.width/4;
			y = mid_y + (y-mid_y)/dist*JOYSTICK.width/4;
		}
		JOYCTX.beginPath();
		JOYCTX.arc(x, y, 10, 0,2*Math.PI, false);// a circle at the start
		JOYCTX.fillStyle = "red";
		JOYCTX.fill();
	}
}

// Use window.requestAnimationFrame, get rid of browser differences.
(function() {
    let lastTime = 0;
    let vendors = ['ms', 'moz', 'webkit', 'o'];
    for(let x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame']
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }
 
    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            let currTime = new Date().getTime();
            let timeToCall = Math.max(0, 16 - (currTime - lastTime));
            let id = window.setTimeout(function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
 
    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());

render();// Render thread
