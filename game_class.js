/*//////////////////////////////////////////////////////////////////////////////////////////////////////
// GAME CLASS
// Holds entities and the game itself
//////////////////////////////////////////////////////////////////////////////////////////////////////*/


function CLASS_game(){
// Private:
	let that = this;
	
	
	//////////////////////////////////////////////////////////////////////////////
	// Savegame section:
	//////////////////////////////////////////////////////////////////////////////
	function CLASS_savegame(){
		this.usernumber = -1;
	
		this.username = null;
		this.password = null;
		this.reached_level = 1;
		
		this.progressed = false;
	
		this.arr_steps = new Array();
		for(let i = 1; i <= 50; i++){
			this.arr_steps[i] = 0;
		}
	}
	
	this.savegame = new CLASS_savegame();
	
	this.clear_savegame = function(){
		this.savegame = new CLASS_savegame();
		that.level_unlocked = 1;
		that.load_level(that.level_unlocked);
	}
	
	this.update_savegame = function(lev, steps){
		if(that.savegame.reached_level <= lev){
			that.savegame.reached_level = lev+1;
			that.savegame.progressed = true;
		}
		if(that.savegame.arr_steps[lev] == 0 || that.savegame.arr_steps[lev] > steps){
			that.savegame.arr_steps[lev] = steps;
			that.savegame.progressed = true;
		}
	}
	
	this.store_savegame = function(){
		if(localStorage.getItem("user_count") === null){
			localStorage.setItem("user_count", 1);
			that.savegame.usernumber = 0;
		}else if(that.savegame.usernumber == -1){
			that.savegame.usernumber = parseInt(localStorage.getItem("user_count"));
			localStorage.setItem("user_count", that.savegame.usernumber+1);
		}
		
		let prefix = "player"+that.savegame.usernumber+"_";
		
		localStorage.setItem(prefix+"username", that.savegame.username);
		localStorage.setItem(prefix+"password", that.savegame.password);
		localStorage.setItem(prefix+"reached_level", that.savegame.reached_level);
		
		for(let i = 1; i <= 50; i++){
			localStorage.setItem(prefix+"steps_lv"+i, that.savegame.arr_steps[i]);
		}
		
		that.savegame.progressed = false;
		
		return ERR_SUCCESS;// Success!
	}
	
	this.retrieve_savegame = function(uname, pass){
		let user_count = localStorage.getItem("user_count");
		if(user_count === null){
			return ERR_NOSAVE;// There are no save games
		}
		user_count = parseInt(user_count);
		pass = md5.digest(pass);
		
		for(let i = 0; i < user_count; i++){
			let prefix = "player"+i+"_";
			if(localStorage.getItem(prefix+"username") == uname){
				if(localStorage.getItem(prefix+"password") == pass){
					that.savegame = new CLASS_savegame();
					that.savegame.usernumber = i;
					that.savegame.username = uname;
					that.savegame.password = pass;
					that.savegame.reached_level = parseInt(localStorage.getItem(prefix+"reached_level"));
					for(let i = 1; i <= 50; i++){
						that.savegame.arr_steps[i] = parseInt(localStorage.getItem(prefix+"steps_lv"+i));
					}
					that.savegame.progressed = false;
					
					that.level_unlocked = that.savegame.reached_level;
					if(that.level_unlocked >= 50){
						that.load_level(50);
					}else{
						that.load_level(that.level_unlocked);
					}
					
					return ERR_SUCCESS;// Success!
				}else{
					return ERR_WRONGPW;// Wrong password!
				}
			}
		}
		return ERR_NOTFOUND;// There's no such name
	}
	
	this.name_savegame = function(uname, pass){
		let user_count = localStorage.getItem("user_count");
		if(user_count !== null){
			user_count = parseInt(user_count);
			for(let i = 0; i < user_count; i++){
				let prefix = "player"+i+"_";
				if(localStorage.getItem(prefix+"username") == uname){
					return ERR_EXISTS;// Failed already exists
				}
			}	
		}
		that.savegame.username = uname;
		that.savegame.password = md5.digest(pass)
		return ERR_SUCCESS;// Worked
	}
	
	this.change_password = function(pass, newpass){
		pass = md5.digest(pass);
		if(that.savegame.password === pass){
			that.savegame.password = md5.digest(newpass);
			localStorage.setItem("player"+that.savegame.usernumber+"_password", that.savegame.password);
			return ERR_SUCCESS;// Worked
		}
		return ERR_WRONGPW;// Wrong pass
	}
	
	// Those calls are on a higher abstraction levels and can be safely used by dialog boxes:
	this.dbxcall_save = function(uname, pass){
		let result;
		if(uname === null || uname == "") {
			vis.error_dbx(ERR_EMPTYNAME);
			return false;
		}
		
		if(that.savegame.username === null){
			result = that.name_savegame(uname, pass);
			if(result != ERR_SUCCESS){
				vis.error_dbx(result);
				return false;
			}
		}
		
		result = that.store_savegame();
		if(result != ERR_SUCCESS){
			vis.error_dbx(result);
			return false;
		}
		
		return true;
	}
	
	this.dbxcall_load = function(uname, pass){
		if(uname === null || uname == "") {
			vis.error_dbx(ERR_EMPTYNAME);
			return false;
		}
		
		let result = that.retrieve_savegame(uname, pass);
		if(result != ERR_SUCCESS){
			vis.error_dbx(result);
			return false;
		}
		
		return true;
	}
	
	this.dbxcall_chpass = function(pass, newpass){
		let result = that.change_password(pass, newpass);
		if(result != ERR_SUCCESS){
			vis.error_dbx(result);
			return false;
		}
		
		return true;
	}
	
	/*//////////////////////////////////////////////////////////////////////////////////////////////////////
	// ENTITY CLASS
	// Players, blocks, opponents. Even dummy block, everything of that is in the entity class.
	//////////////////////////////////////////////////////////////////////////////////////////////////////*/
	
	function CLASS_entity(){
	}
	CLASS_entity.prototype.init = function(a_id){
	// Public:
		this.id = a_id
		this.moving = false;
		this.moving_offset = {x: 0, y: 0};
		this.pushing = false;
		this.face_dir = DIR_DOWN;
		this.berti_id = -1;// Multiple bertis are possible, this makes the game engine much more flexible
		this.sees_berti = false;
		this.time_since_noise = 100;
		this.just_moved = false;
		this.gets_removed_in = -1;// Removal timer for doors
		
		if(this.id == ENT_PLAYER_BERTI || this.id == ENT_AUTO_BERTI || this.id == ENT_LIGHT_BLOCK || this.id == ENT_PURPLE_MONSTER){
			this.can_push = true;
		}else{
			this.can_push = false;
		}
		
		if(this.id == ENT_LIGHT_BLOCK || this.id == ENT_HEAVY_BLOCK){
			this.pushable = true;
		}else{
			this.pushable = false;
		}
		
		if(this.id == ENT_BANANA_PEEL || this.id == ENT_KEY_1 || this.id == ENT_KEY_2 || this.id == ENT_KEY_3 || this.id == ENT_KEY_4 || this.id == ENT_KEY_5 || this.id == ENT_KEY_6){
			this.consumable = true;
		}else{
			this.consumable = false;
		}
		
		if(this.id == ENT_PLAYER_BERTI || this.id == ENT_AUTO_BERTI || this.id == ENT_PURPLE_MONSTER || this.id == ENT_GREEN_MONSTER){
			// This is a technical attribute.
			// Small entities can follow into occupied, moving entities from all directions.
			// Monsters can see through small entities.
			this.is_small = true;
		}else{
			this.is_small = false;
		}
		
		// Purely visual aspects here. No impact on gameplay logic
		this.animation_frame = -1;
		this.animation_delay = 0;
		
		this.fine_offset_x = 0;
		this.fine_offset_y = 0;
		// end visual
	}
	CLASS_entity.prototype.move_randomly = function(curr_x, curr_y){
		if(!this.moving){
			let tried_forward = false;
			let back_dir = game.opposite_dir(this.face_dir);
			let possibilities = new Array(DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT);
			for(let i = 0; i < possibilities.length; i++){
				if(possibilities[i] == this.face_dir || possibilities[i] == back_dir){
					possibilities.splice(i, 1);
					i--;
				}
			}
			
			if(Math.random() < 0.80){
				if(game.walkable(curr_x, curr_y, this.face_dir)){
					game.start_move(curr_x, curr_y, this.face_dir);
					return;
				}
				tried_forward = true;
			}
			
			while(possibilities.length > 0){
				let selection = Math.floor(Math.random()*possibilities.length);
				if(game.walkable(curr_x, curr_y, possibilities[selection])){
					game.start_move(curr_x, curr_y, possibilities[selection]);
					return;
				}else{
					possibilities.splice(selection, 1);
				}
			}
			
			if(!tried_forward){
				if(game.walkable(curr_x, curr_y, this.face_dir)){
					game.start_move(curr_x, curr_y, this.face_dir);
					return;
				}
			}
			
			if(game.walkable(curr_x, curr_y, back_dir)){
				game.start_move(curr_x, curr_y, back_dir);
				return;
			}
			// Here's the code if that dude can't go anywhere: (none)
		}
	}
	CLASS_entity.prototype.chase_berti = function(curr_x, curr_y){
		if(!this.moving){
			this.time_since_noise++;
			
			let closest_dist = LEV_DIMENSION_X + LEV_DIMENSION_Y + 1;
			let closest_berti = -1;
			
			for(let i = 0; i < game.berti_positions.length; i++){
				let face_right_direction = 
				(this.face_dir == DIR_DOWN && game.berti_positions[i].y >= curr_y) || 
				(this.face_dir == DIR_UP && game.berti_positions[i].y <= curr_y) || 
				(this.face_dir == DIR_LEFT && game.berti_positions[i].x <= curr_x) || 
				(this.face_dir == DIR_RIGHT && game.berti_positions[i].x >= curr_x);
				
				if(face_right_direction && game.can_see_tile(curr_x, curr_y, game.berti_positions[i].x, game.berti_positions[i].y)){
					let distance = Math.abs(game.berti_positions[i].x - curr_x) + Math.abs(game.berti_positions[i].y - curr_y);// Manhattan distance
					if(distance < closest_dist || (distance == closest_dist && Math.random() < 0.50)){
						closest_dist = distance;
						closest_berti = i;
					}
				}
			}
			
			if(closest_berti == -1 || Math.random() < 0.02){// Can't see berti OR he randomly gets distracted THEN Random search
				this.sees_berti = false;
				this.move_randomly(curr_x, curr_y);
			}else{// Chasing code here.
				if(!this.sees_berti){
					this.sees_berti = true;
					
					if(this.time_since_noise > Math.ceil(Math.random()*10)+3){
						this.time_since_noise = 0;
						if(this.id == ENT_PURPLE_MONSTER){
							game.play_sound(2);
						}else if(this.id == ENT_GREEN_MONSTER){
							game.play_sound(3);
						}
					}
				}
				
				let diff_x = game.berti_positions[closest_berti].x - curr_x;
				let diff_y = game.berti_positions[closest_berti].y - curr_y;
				
				// THIS IS AN OPTIONAL FIX THAT MAKES THE GAME MUCH HARDER!
				/*let closest_berti_obj = game.level_array[game.berti_positions[closest_berti].x][game.berti_positions[closest_berti].y];
				
				if(closest_berti_obj.moving){
					let next_pos = game.dir_to_coords(game.berti_positions[closest_berti].x, game.berti_positions[closest_berti].y, closest_berti_obj.face_dir);
					if(Math.abs(curr_x - next_pos.x) + Math.abs(curr_y - next_pos.y) == 1){
						if(Math.abs(closest_berti_obj.moving_offset.x) + Math.abs(closest_berti_obj.moving_offset.x) >= 15)
						return;
					}
				}*/// END OF OPTIONAL FIX
				
				let dir1;
				let dir2;
				
				if(diff_x == 0){
					if(diff_y == 0){// This should NEVER happen.
						alert("001: Something went mighty wrong! Blame the programmer!");
						this.move_randomly(curr_x, curr_y);
						return;
					}else if(diff_y > 0){
						dir1 = dir2 = DIR_DOWN;
					}else{// diff_y < 0
						dir1 = dir2 = DIR_UP;
					}
				}else if(diff_x > 0){
					if(diff_y == 0){
						dir1 = dir2 = DIR_RIGHT;
					}else if(diff_y > 0){
						dir1 = DIR_RIGHT;
						dir2 = DIR_DOWN;
					}else{// diff_y < 0
						dir1 = DIR_RIGHT
						dir2 = DIR_UP;
					}
				}else{// diff_x < 0
					if(diff_y == 0){
						dir1 = dir2 = DIR_LEFT;
					}else if(diff_y > 0){
						dir1 = DIR_LEFT;
						dir2 = DIR_DOWN;
					}else{// diff_y < 0
						dir1 = DIR_LEFT
						dir2 = DIR_UP;
					}
				}
				
				if(dir1 != dir2){
					let total_distance = Math.abs(diff_x) + Math.abs(diff_y);
					let percentage_x = Math.abs(diff_x / total_distance);
					
					if(Math.random() >= percentage_x){
						let swapper = dir1;
						dir1 = dir2;
						dir2 = swapper;
					}
					if(game.walkable(curr_x, curr_y, dir1)){
						game.start_move(curr_x, curr_y, dir1);
					}else if(game.walkable(curr_x, curr_y, dir2)){
						game.start_move(curr_x, curr_y, dir2);
					}else{
						this.move_randomly(curr_x, curr_y);
					}
				}else{
					if(game.walkable(curr_x, curr_y, dir1)){
						game.start_move(curr_x, curr_y, dir1);
					}else{
						this.move_randomly(curr_x, curr_y);
					}
				}
				
			}
		}
	}
	
	CLASS_entity.prototype.update_entity = function(curr_x, curr_y){
		this.animation_delay++;// This is an important link between the game logic and animation timing.
		
		if(this.moving){
			switch (this.face_dir) {
				case DIR_UP:
					this.moving_offset.y -= game.move_speed;
					break;
				case DIR_DOWN:
					this.moving_offset.y += game.move_speed;
					break;
				case DIR_LEFT:
					this.moving_offset.x -= game.move_speed;
					break;
				case DIR_RIGHT:
					this.moving_offset.x += game.move_speed;
					break;
				default:
					alert("002: Something went mighty wrong! Blame the programmer!");// This should never be executed
					break;
			}
			if(this.moving_offset.x <= -24 || this.moving_offset.x >= 24 || this.moving_offset.y <= -24 || this.moving_offset.y >= 24){
				game.move(curr_x, curr_y, this.face_dir);
				this.just_moved = true;
			}
		}
		
		if(this.gets_removed_in == 0){
			if(this.moving){
				let dst = game.dir_to_coords(curr_x, curr_y, this.face_dir);
				game.level_array[dst.x][dst.y].init(ENT_EMPTY);
			}
			game.level_array[curr_x][curr_y].init(ENT_EMPTY);
		}else if(this.gets_removed_in > 0){
			this.gets_removed_in -= 1;
			vis.update_animation(curr_x, curr_y);
		}
	}
	
	CLASS_entity.prototype.register_input = function(curr_x, curr_y, just_prime){
		if(!this.moving){
			for(let i = 0; i < 3; i++){
				let dir_1 = DIR_NONE;
				let dir_2 = DIR_NONE;
				if(i == 0){
					// Keyboard control
					if(input.keys_down[KEY_CODE_LEFT] && !input.keys_down[KEY_CODE_RIGHT]){
						dir_1 = DIR_LEFT;
					}else if(!input.keys_down[KEY_CODE_LEFT] && input.keys_down[KEY_CODE_RIGHT]){
						dir_1 = DIR_RIGHT;
					}
					
					if(input.keys_down[KEY_CODE_UP] && !input.keys_down[KEY_CODE_DOWN]){
						dir_2 = DIR_UP;
					}else if(!input.keys_down[KEY_CODE_UP] && input.keys_down[KEY_CODE_DOWN]){
						dir_2 = DIR_DOWN;
					}
					
					if(game.last_dir_pressed == DIR_UP || game.last_dir_pressed == DIR_DOWN){
						// Make sure that the preferred direction is what we last pressed
						let swap_helper = dir_1;
						dir_1 = dir_2;
						dir_2 = swap_helper;
					}
					
				}else if(i == 1){
					// Touch control
					if(IS_TOUCH_DEVICE){
						dir_1 = input.joystick_dir;
					}
				}else if(i == 2){
					// Auto walk control
					if(!game.single_steps){
						dir_1 = game.last_dir_pressed;
					}
				}
				
				for(let j = 0; j < 2; j++){
					let dir = DIR_NONE;
					if(j == 0){
						dir = dir_1;
					}else if(j == 1){
						dir = dir_2;
					}
					if(!just_prime && game.walkable(curr_x, curr_y, dir)){
						game.start_move(curr_x, curr_y, dir);
						return;
					}
				}
			}
		}
	}
	// After each update, this function gets called for (every) Berti to see if he was caught!
	CLASS_entity.prototype.check_enemy_proximity = function(curr_x, curr_y){
		
		if(this.moving_offset.x != 0 || this.moving_offset.y != 0) return;
		
		let adj_array = game.get_adjacent_tiles(curr_x, curr_y);
		for(let i = 0; i < adj_array.length; i++){
			if(game.level_array[adj_array[i].x][adj_array[i].y].id == ENT_PURPLE_MONSTER || game.level_array[adj_array[i].x][adj_array[i].y].id == ENT_GREEN_MONSTER){// If there's an opponent on this adjacent tile
				let enemy_moving_offset_x = game.level_array[adj_array[i].x][adj_array[i].y].moving_offset.x;
				let enemy_moving_offset_y = game.level_array[adj_array[i].x][adj_array[i].y].moving_offset.y;
				if(enemy_moving_offset_x != 0 || enemy_moving_offset_y != 0) continue;
				
				if(Math.abs(curr_x - adj_array[i].x) == 1 && Math.abs(curr_y - adj_array[i].y) == 1){// If the opponent is diagonally AND
					// there's an obstacle in the way
					if((game.level_array[adj_array[i].x][curr_y].id != ENT_DUMMY && game.level_array[adj_array[i].x][curr_y].id != ENT_EMPTY) ||
						(game.level_array[curr_x][adj_array[i].y].id != ENT_DUMMY && game.level_array[curr_x][adj_array[i].y].id != ENT_EMPTY)){
						continue;// Don't perform a proximity check for this particular foe.
					}
				}
			
				// Got caught!
				game.play_sound(1);
				game.wait_timer = LEV_STOP_DELAY*UPS;
				game.level_ended = 2;
				vis.update_all_animations();
				return;
			}
		}
	}

	/*//////////////////////////////////////////////////////////////////////////////////////////////////////
	// END OF ENTITY CLASS
	// GAME CLASS
	// Core engine, entity class, game ending criteria and much more
	//////////////////////////////////////////////////////////////////////////////////////////////////////*/
	this.move_speed = Math.round(1*60/UPS);
	this.door_removal_delay = Math.round(8*UPS/60);
	
	this.fpsInterval = 1000 / UPS;
	this.then = Date.now();
	
	this.initialized = false;
	this.wait_timer = INTRO_DURATION*UPS;
	this.paused = false;
	
	this.update_drawn = false;
	this.mode = 0;// 0 is entry, 1 is menu and play
	this.level_number = 0;
	this.level_array = new Array();
	this.level_unlocked = 0;
	this.level_ended = 0;// 0 is not ended. 1 is won. 2 is died.
	this.wow = true;// true is WOW!, false is Yeah!
	
	this.berti_positions;
	
	this.single_steps = true;
	this.last_dir_pressed = DIR_NONE;
	
	this.steps_taken = 0;
	this.num_bananas = 0;
	
	this.last_updated = Date.now();
	this.delta_updated = 0;
	
	this.buttons_activated = new Array();
	this.buttons_activated[0] = this.buttons_activated[2] = false;
	this.buttons_activated[1] = true;
	
	this.sound = !DEBUG;
	this.soundrestriction_removed = false;
	
	this.update_tick = 0;
	
	this.load_level = function(lev_number){
		that.mode = 1;
		that.update_tick = 0;
	
		that.steps_taken = 0;
		that.num_bananas = 0;
		that.level_ended = 0;
		that.level_array = new Array();
		that.level_number = lev_number;
		that.wait_timer = LEV_START_DELAY*UPS;
		that.last_dir_pressed = DIR_NONE;
		
		if(that.level_unlocked < lev_number){
			that.level_unlocked = lev_number;
		}
		
		if(lev_number < that.level_unlocked && lev_number != 0){
			that.buttons_activated[2] = true;
		}else{
			that.buttons_activated[2] = false;
		}
		
		if(lev_number > 1){
			that.buttons_activated[0] = true;
		}else{
			that.buttons_activated[0] = false;
		}
		
		for(let i = 0; i < LEV_DIMENSION_X; i++){
			that.level_array[i] = new Array()
		}
		
		let berti_counter = 0;
		that.berti_positions = new Array();
		
		for(let y = 0; y < LEV_DIMENSION_Y; y++){
			for(let x = 0; x < LEV_DIMENSION_X; x++){
				that.level_array[x][y] = new CLASS_entity();
				that.level_array[x][y].init(res.levels[lev_number][x][y]);
				
				if(res.levels[lev_number][x][y] == 4){
					that.num_bananas++;
				}else if(res.levels[lev_number][x][y] == 1){
					that.level_array[x][y].berti_id = berti_counter;
					that.berti_positions[berti_counter] = {x: x, y: y};
					berti_counter++;
				}
			}
		}
		
		vis.init_animation();
		
		if(berti_counter > 0){
			that.play_sound(8);
		}
	}
	
	this.remove_door = function(id){
		that.play_sound(9);
		for(let y = 0; y < LEV_DIMENSION_Y; y++){
			for(let x = 0; x < LEV_DIMENSION_X; x++){
				if(that.level_array[x][y].id == id){
					that.level_array[x][y].gets_removed_in = that.door_removal_delay;
				}					
			}
		}
	}
	// Whether you can walk from a tile in a certain direction, boolean
	this.walkable = function(curr_x, curr_y, dir){
		
		let dst = that.dir_to_coords(curr_x, curr_y, dir);
		
		if(!this.is_in_bounds(dst.x, dst.y)){// Can't go out of boundaries
			return false;
		}
		
		if(that.level_array[dst.x][dst.y].id == ENT_EMPTY){
			// Blank space is always walkable
			return true;
		}else if(!that.level_array[dst.x][dst.y].moving){
			if((that.level_array[curr_x][curr_y].id == ENT_PLAYER_BERTI || that.level_array[curr_x][curr_y].id == ENT_AUTO_BERTI) && that.level_array[dst.x][dst.y].consumable){
				// Can pick up items.
				return true;
			}else{
				if(that.level_array[curr_x][curr_y].can_push == 1 && that.level_array[dst.x][dst.y].pushable == 1){
					return that.walkable(dst.x, dst.y, dir);
				}else{
					return false;
				}
			}
		}else if( // (the entity at the destination is moving)
			that.level_array[dst.x][dst.y].face_dir == dir || // If the entity is already moving away in the right direction or...
			that.level_array[curr_x][curr_y].is_small && that.level_array[dst.x][dst.y].is_small){ // ...the tile is about to be freed by a small entity
			
			let adj_array = that.get_adjacent_tiles_primary(dst.x, dst.y);
			for(let i = 0; i < adj_array.length; i++){
				if(that.level_array[adj_array[i].x][adj_array[i].y].moving){
					let dst2 = that.dir_to_coords(adj_array[i].x, adj_array[i].y, that.level_array[adj_array[i].x][adj_array[i].y].face_dir)
					if(dst.x == dst2.x && dst.y == dst2.y){ // Someone is already moving into the tile we want to move to
						return false;
					}
				}
			}
			return true;
		}else{
			return false;
		}
	}
	
	this.start_move = function(src_x, src_y, dir){
	
		let dst = that.dir_to_coords(src_x, src_y, dir);
		that.level_array[src_x][src_y].moving = true;
		that.level_array[src_x][src_y].face_dir = dir;
		
		if(that.level_array[src_x][src_y].id == ENT_PLAYER_BERTI){
			if(that.steps_taken < 99999){
				that.steps_taken++;
			}
		}
		
		if((that.level_array[src_x][src_y].id == ENT_PLAYER_BERTI || that.level_array[src_x][src_y].id == ENT_AUTO_BERTI) && that.level_array[dst.x][dst.y].consumable){
			// Om nom nom start
		}else if(that.level_array[dst.x][dst.y].moving){
			// It's moving out of place by itself, don't do anything
		}else if(that.level_array[dst.x][dst.y].id != ENT_EMPTY){
			that.level_array[src_x][src_y].pushing = true;
			that.start_move(dst.x, dst.y, dir);
		}else{
			that.level_array[dst.x][dst.y].init(ENT_DUMMY); // Reserve square with dummy block
		}
		
		vis.update_animation(src_x,src_y);
	}
	
	this.move = function(src_x, src_y, dir){
	
		let dst = that.dir_to_coords(src_x, src_y, dir);
		that.level_array[src_x][src_y].moving = false;
		that.level_array[src_x][src_y].moving_offset = {x: 0, y: 0};
		that.level_array[src_x][src_y].pushing = false;
		
		if((that.level_array[src_x][src_y].id == ENT_PLAYER_BERTI || that.level_array[src_x][src_y].id == ENT_AUTO_BERTI) && that.level_array[dst.x][dst.y].consumable){
			switch (that.level_array[dst.x][dst.y].id) {// Done Om nom nom
				case ENT_BANANA_PEEL:
					that.num_bananas--;
					if(that.num_bananas <= 0){
						that.wait_timer = LEV_STOP_DELAY*UPS;
						that.level_ended = 1;
						if(Math.random() < 0.50){
							game.wow = true;
							that.play_sound(10);// wow
						}else{
							game.wow = false;
							that.play_sound(11);// yeah
						}
						vis.update_all_animations();
					}else{
						that.play_sound(7);// Om nom nom
					}
					break;
				case ENT_KEY_1:
					that.remove_door(ENT_DOOR_1);
					break;
				case ENT_KEY_2:
					that.remove_door(ENT_DOOR_2);
					break;
				case ENT_KEY_3:
					that.remove_door(ENT_DOOR_3);
					break;
				case ENT_KEY_4:
					that.remove_door(ENT_DOOR_4);
					break;
				case ENT_KEY_5:
					that.remove_door(ENT_DOOR_5);
					break;
				case ENT_KEY_6:
					that.remove_door(ENT_DOOR_6);
					break;
				default:
					alert("003: Something went mighty wrong! Blame the programmer!");
					break;
			 }
		}else if(that.level_array[dst.x][dst.y].id != ENT_DUMMY && that.level_array[dst.x][dst.y].id != ENT_EMPTY){
			that.move(dst.x, dst.y, dir);
		}else if(that.sound){// we need another logic to determine this correctly...DEBUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			let dst2 = that.dir_to_coords(dst.x, dst.y, dir);
			if(	(that.level_array[src_x][src_y].id == ENT_LIGHT_BLOCK || that.level_array[src_x][src_y].id == ENT_HEAVY_BLOCK) &&
				(!that.is_in_bounds(dst2.x, dst2.y) || that.level_array[dst2.x][dst2.y].id == ENT_PINNED_BLOCK)){
				that.play_sound(5);
			}
		}
		let swapper = that.level_array[dst.x][dst.y];
		that.level_array[dst.x][dst.y] = that.level_array[src_x][src_y];
		that.level_array[src_x][src_y] = swapper;
		
		let back_dir = that.opposite_dir(dir);
		let before_src = that.dir_to_coords(src_x, src_y, back_dir);
		
		let possibilities = new Array(DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT);
		for(let i = 0; i < possibilities.length; i++){
			if(possibilities[i] == dir || possibilities[i] == back_dir){
				possibilities.splice(i, 1);
				i--;
			}
		}
		let before_src2 = that.dir_to_coords(src_x, src_y, possibilities[0]);
		let before_src3 = that.dir_to_coords(src_x, src_y, possibilities[1]);
		
		if(
		(that.is_in_bounds(before_src.x, before_src.y) && (that.level_array[before_src.x][before_src.y].moving && that.level_array[before_src.x][before_src.y].face_dir == dir)) ||
		that.level_array[dst.x][dst.y].is_small && ((that.is_in_bounds(before_src2.x, before_src2.y) && (that.level_array[before_src2.x][before_src2.y].is_small &&  that.level_array[before_src2.x][before_src2.y].moving && that.level_array[before_src2.x][before_src2.y].face_dir == possibilities[1])) ||
		(that.is_in_bounds(before_src3.x, before_src3.y) && (that.level_array[before_src3.x][before_src3.y].is_small &&  that.level_array[before_src3.x][before_src3.y].moving && that.level_array[before_src3.x][before_src3.y].face_dir == possibilities[0])))
		){
			that.level_array[src_x][src_y].init(ENT_DUMMY);
		}else{		
			that.level_array[src_x][src_y].init(ENT_EMPTY);
		}
		
		if(that.level_array[dst.x][dst.y].id == ENT_PLAYER_BERTI){// Rectify the position of Berti
			that.berti_positions[that.level_array[dst.x][dst.y].berti_id] = dst;
		}
	}
	
	this.dir_to_coords = function(curr_x, curr_y, dir){
		let new_x = curr_x;
		let new_y = curr_y;
		
		switch (dir) {
			case DIR_UP:
				new_y--;
				break;
			case DIR_DOWN:
				new_y++;
				break;
			case DIR_LEFT:
				new_x--;
				break;
			case DIR_RIGHT:
				new_x++;
				break;
			default:
				break;
		}
		return {x: new_x, y: new_y};
	}
	
	this.opposite_dir = function(dir){
		switch (dir) {
			case DIR_UP:
				return DIR_DOWN;
				break;
			case DIR_DOWN:
				return DIR_UP;
				break;
			case DIR_LEFT:
				return DIR_RIGHT;
				break;
			case DIR_RIGHT:
				return DIR_LEFT;
				break;
			default:
				return DIR_NONE
				break;
		}
	}
	
	this.get_adjacent_tiles = function(tile_x, tile_y){// Potential for optimization
		//let result; = new Array();

		//if(tile_x-1 >= 0 && tile_y-1 >= 0 && tile_x+1 < LEV_DIMENSION_X && tile_y+1 < LEV_DIMENSION_Y){
		//	return new Array({x:tile_x-1, y:tile_y-1}, {x:tile_x-1, y:tile_y}, {x:tile_x-1, y:tile_y+1}, {x:tile_x, y:tile_y-1}, {x:tile_x, y:tile_y+1}, {x:tile_x+1, y:tile_y-1}, {x:tile_x+1, y:tile_y}, {x:tile_x+1, y:tile_y+1});
		//}else{
			let result = new Array();
			for(let i = -1; i <= 1; i++){
				for(let j = -1; j <= 1; j++){
					if(i != 0 || j != 0){
						if(that.is_in_bounds(tile_x+i, tile_y+j)){
							result.push({x:(tile_x+i), y:(tile_y+j)});
						}
					}
				}
			}
			return result;
		//}
		
	}
	
	this.get_adjacent_tiles_primary = function(tile_x, tile_y){ // Primary neighborhood (up, down, left, right but no diagonals)
		let result = new Array();
		if(that.is_in_bounds(tile_x, tile_y-1)){
			result.push({x:(tile_x), y:(tile_y-1)});
		}
		if(that.is_in_bounds(tile_x, tile_y+1)){
			result.push({x:(tile_x), y:(tile_y+1)});
		}
		if(that.is_in_bounds(tile_x-1, tile_y)){
			result.push({x:(tile_x-1), y:(tile_y)});
		}
		if(that.is_in_bounds(tile_x+1, tile_y)){
			result.push({x:(tile_x+1), y:(tile_y)});
		}
		return result;
	}
	
	this.is_in_bounds = function(tile_x, tile_y){
		return (tile_x >= 0 && tile_y >= 0 && tile_x < LEV_DIMENSION_X && tile_y < LEV_DIMENSION_Y);
	}
	
	this.can_see_tile = function(eye_x, eye_y, tile_x, tile_y){
		let diff_x = tile_x - eye_x;
		let diff_y = tile_y - eye_y;
		
		let walk1_x;
		let walk1_y;
		let walk2_x;
		let walk2_y;
		
		if (diff_x==0){
			if(diff_y==0){
				return true;
			}else if(diff_y > 0){
				walk1_x = 0;
				walk1_y = 1;
				walk2_x = 0;
				walk2_y = 1;
			}else{// diff_y < 0
				walk1_x = 0;
				walk1_y = -1;
				walk2_x = 0;
				walk2_y = -1;
			}
		}else if(diff_x > 0){
			if(diff_y==0){
				walk1_x = 1;
				walk1_y = 0;
				walk2_x = 1;
				walk2_y = 0;
			}else if(diff_y > 0){
				if(diff_y > diff_x){
					walk1_x = 0;
					walk1_y = 1;
					walk2_x = 1;
					walk2_y = 1;
				}else if(diff_y == diff_x){
					walk1_x = 1;
					walk1_y = 1;
					walk2_x = 1;
					walk2_y = 1;
				}else{// diff_y < diff_x
					walk1_x = 1;
					walk1_y = 0;
					walk2_x = 1;
					walk2_y = 1;
				}
			}else{// diff_y < 0
				if(diff_y*(-1) > diff_x){
					walk1_x = 0;
					walk1_y = -1;
					walk2_x = 1;
					walk2_y = -1;
				}else if(diff_y*(-1) == diff_x){
					walk1_x = 1;
					walk1_y = -1;
					walk2_x = 1;
					walk2_y = -1;
				}else{// diff_y < diff_x
					walk1_x = 1;
					walk1_y = 0;
					walk2_x = 1;
					walk2_y = -1;
				}
			}
		}else{// diff_x < 0
			if(diff_y==0){
				walk1_x = -1;
				walk1_y = 0;
				walk2_x = -1;
				walk2_y = 0;
			}else if(diff_y > 0){
				if(diff_y > diff_x*(-1)){
					walk1_x = 0;
					walk1_y = 1;
					walk2_x = -1;
					walk2_y = 1;
				}else if(diff_y == diff_x*(-1)){
					walk1_x = -1;
					walk1_y = 1;
					walk2_x = -1;
					walk2_y = 1;
				}else{// diff_y < diff_x
					walk1_x = -1;
					walk1_y = 0;
					walk2_x = -1;
					walk2_y = 1;
				}
			}else{// diff_y < 0
				if(diff_y > diff_x){
					walk1_x = -1;
					walk1_y = 0;
					walk2_x = -1;
					walk2_y = -1;
				}else if(diff_y == diff_x){
					walk1_x = -1;
					walk1_y = -1;
					walk2_x = -1;
					walk2_y = -1;
				}else{// diff_y < diff_x
					walk1_x = 0;
					walk1_y = -1;
					walk2_x = -1;
					walk2_y = -1;
				}
			}
		}
		
		
		let x_offset = 0;
		let y_offset = 0;
		let x_ratio1;
		let y_ratio1;
		let x_ratio2;
		let y_ratio2;
		let diff1;
		let diff2;
		
		while(true){
			if(diff_x != 0){
				x_ratio1 = (x_offset+walk1_x)/diff_x;
				x_ratio2 = (x_offset+walk2_x)/diff_x;
			}else{
				x_ratio1 = 1;
				x_ratio2 = 1;
			}
			if(diff_y != 0){
				y_ratio1 = (y_offset+walk1_y)/diff_y;
				y_ratio2 = (y_offset+walk2_y)/diff_y;
			}else{
				y_ratio1 = 1;
				y_ratio2 = 1;
			}
			
			diff1 = Math.abs(x_ratio1-y_ratio1);
			diff2 = Math.abs(x_ratio2-y_ratio2);
			
			if (diff1 <= diff2){
				x_offset += walk1_x;
				y_offset += walk1_y;
			}else{
				x_offset += walk2_x;
				y_offset += walk2_y;
			}
			
			if(x_offset == diff_x && y_offset == diff_y){
				return true;
			}
			if(game.level_array[eye_x + x_offset][eye_y + y_offset].id != ENT_EMPTY && game.level_array[eye_x + x_offset][eye_y + y_offset].id != ENT_DUMMY && !game.level_array[eye_x + x_offset][eye_y + y_offset].is_small){
				return false;
			}
		}
		// Code here is unreachable
	}
	
	this.prev_level = function(){
		if(that.level_number >= 1){
			that.load_level(that.level_number-1);
		}
	}
	
	this.next_level = function(){
		if(that.level_number >= 50 || that.level_number < 0){
			game.mode = 2;
			game.steps_taken = 0;
			game.play_sound(6);
			that.buttons_activated[0] = false;
			that.buttons_activated[2] = false;
			return;
		}
		that.load_level(that.level_number+1);// Prevent overflow here
		if(that.level_number > that.level_unlocked){
			that.level_unlocked = that.level_number;
		}
	}
	
	this.reset_level = function(){
		if(that.mode == 0){
			that.load_level(0);
		}else if(that.mode == 1){
			if(that.level_number == 0){
				that.load_level(1);
			}else{
				that.load_level(that.level_number);
			}
		}
	}
	
	this.play_sound = function(id){
		if(!that.sound) return;
		if(res.sounds[id].currentTime!=0) res.sounds[id].currentTime=0;
		res.sounds[id].play();
		// Useful commands
		//audioElement.pause();
		//audioElement.volume=0;
		//audioElement.src;
		//audioElement.duration;
		//myAudio.addEventListener('ended', function() {}, false);
	}
	
	this.set_volume = function(vol){
		if(vol > 1){
			vol = 1;
		}else if(vol < 0){
			vol = 0;
		}
		vis.vol_bar.volume = vol;
		vol = Math.pow(vol, 3);// LOGARITHMIC!
	
		for(let i = 0; i < res.sounds.length; i++){
			res.sounds[i].volume = vol;
		}
	}
	
	this.toggle_sound = function(){
		if(that.sound){
			that.sound = false;
			for(let i = 0; i < res.sounds.length; i++){
				res.sounds[i].pause();
				res.sounds[i].currentTime=0
			}
		}else{
			that.sound = true;
		}
	}
	
	// This is necessary because of mobile browsers. These browsers block sound playback
	// unless it is triggered by a user input event. Play all sounds at the first input,
	// then the restriction is lifted for further playbacks.
	this.remove_soundrestriction = function(){
		if(that.soundrestriction_removed) return;
		for(let i = 0; i < res.sounds.length; i++){
			if(res.sounds[i].paused) {
				res.sounds[i].play();
				res.sounds[i].pause();
				res.sounds[i].currentTime=0
			}
		}
		that.soundrestriction_removed = true;
	}
	
	this.toggle_single_steps = function(){
		if(that.single_steps){
			that.last_dir_pressed = DIR_NONE;
			that.single_steps = false;
		}else{
			that.single_steps = true;
		}
	}
	
	this.toggle_paused = function(){
		if(that.paused){
			that.paused = false;
		}else{
			that.paused = true;
		}
	}
}