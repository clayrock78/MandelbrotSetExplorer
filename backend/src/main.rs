/* * * * * * * * * * * * * * * * * * * * * *
v1 * Written by Clayton Jones * 10-29-21 to 11-9-21 
Rust Translation / Remake of a Mandelbrot image generator
(originally made in Python, using turtle)
 * * * * * * * * * * * * * * * * * * * * * */

extern crate image;
use image::{ImageBuffer, RgbImage};
use palette::{Srgb, Hsv, Pixel, IntoColor};
use std::fs;
use std::env;

fn interp_x(n : u32, XLO : f64, XHI : f64, scale : u32) -> f64 {
	// Screen size definitions (pixels)
	let LO_IN : f64 = 0.0;
	let HI_IN : f64 = scale as f64;

	// Calculate the slope
	let slope : f64 = (XHI - XLO) / (HI_IN - LO_IN);

	// Plug slope into equation y = mx + b
	slope * ((n as f64) - LO_IN) + XLO
}


fn interp_y(n : u32, YLO : f64, YHI : f64, scale : u32) -> f64 { 
	// Screen size definitions (pixels)
	let LO_IN : f64 = 0.0;
	let HI_IN : f64 = scale as f64;

	// Calculate the slope
	let slope : f64 = (YHI - YLO) / (HI_IN - LO_IN);

	// Plug slope into equation y = mx + b
	slope * ((n as f64) - LO_IN) + YLO
}

fn main(){
	// Get path (probably the dumbest way to do this)
	let mut path: String = "".to_string();
	let args = env::args();
	for argument in args {
		path = argument.replace("\\target\\release\\my-project.exe", "");
	}
	let final_path : &str = &*path;

	// Create window information based on file data
	let raw_contents : String = fs::read_to_string(final_path.to_owned() + "\\bounds.txt").unwrap();
	let content_list : Vec<f64> = raw_contents
		.split(",")
		.map(|x|
			x.parse::<f64>()
			.unwrap())
			.collect();

	let XLO : f64 = content_list[0];
	let XHI : f64 = content_list[1]; 

	let YLO : f64 = content_list[2]; 
	let YHI : f64 = content_list[3]; 

	let max_i : u32 = content_list[4] as u32;
	let scale : u32 = content_list[5] as u32;

	// Create an image
	let mut image: RgbImage = ImageBuffer::new(scale, scale);

	let mut lines_drawn : i32 = 0;
	let mut percent_finished : i8 = 0;

	// iterating through x pixel values
	for x in 0..scale{

		// iterating through y pixel values

		for y in 0..scale{

			// finding scaled pixel values
			let scaled_x = interp_x(x as u32, XLO, XHI,scale);
			let scaled_y = interp_y(y as u32, YLO, YHI,scale);

			let mut i : u32 = 0;
			
			// Stopping ourself from calculating anything within the main cardiod
			let p = (scaled_x - 0.25).powi(2) + scaled_y.powi(2);
			let o = 0.25 * scaled_y.powi(2);
			if p*(p + (scaled_x - 0.25)) <= o {
				let color = Hsv::new(360.0, 0.3, 0.0);
				let srgb: Srgb = color.into_color();

				let colorarr: [u8; 3] = Srgb::into_linear(srgb)
					.into_format()
					.into_raw();
				
				*image.get_pixel_mut(x.into(), y.into()) = image::Rgb(colorarr);
				continue;
			}

			// X and Y calculation values
			let mut x1 : f64;
			let mut y1 : f64;

			// Squares of x and y values
			let mut x2 : f64 = 0.0;
			let mut y2 : f64 = 0.0;
			
			let mut w : f64 = 0.0;

			while (x2 + y2 <= 4.0) && (i < max_i) {
				x1 = x2 - y2 + scaled_x;
				y1 = w - x2 - y2 + scaled_y;
				x2 = x1*x1;
				y2 = y1*y1;
				w = (x1+y1).powi(2);
				i += 1;
			}
			let hue : f32 = (i % 360) as f32;

			let bit = if i >= max_i {
				0.0
			} else {
				0.8
			};

			let color = Hsv::new(hue, 0.7, bit);

			let srgb: Srgb = color.into_color();

			let colorarr: [u8; 3] = Srgb::into_linear(srgb)
				.into_format()
				.into_raw();
			
			*image.get_pixel_mut(x.into(), y.into()) = image::Rgb(colorarr);
		}
		lines_drawn += 1;
		if lines_drawn == ((scale as i32) / 100) {
			percent_finished += 1; lines_drawn = 0;
		}
	}
	let mut final_path;

	if (scale == 2000) {
		final_path = path.to_owned().replace("\\backend", "") + "\\RENDEREDmandel.png";
	} else {
		final_path = path.to_owned() + "\\mandel.png";
	}
	
	image.save(final_path).unwrap();
}