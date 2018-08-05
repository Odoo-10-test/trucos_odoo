/**********************************************************************************
* 
*    Copyright (C) 2017 MuK IT GmbH
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as
*    published by the Free Software Foundation, either version 3 of the
*    License, or (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
**********************************************************************************/

odoo.define('muk_website_snippet_particles.frontend', function (require) {
'use strict';

var base = require('web_editor.base');
var core = require('web.core');

var QWeb = core.qweb;
var _t = core._t;

var ParticleSnippet = core.Class.extend({
	init: function($particles) {
		this.$particles = $particles;
	},
	parseAttr: function(text) {
		try {
			return $.parseJSON(text);
		} catch(err) {
			return text;
		}
	},
	create_particles: function() {
		this.model = {
			"particles": {
				"number": {
			      "value": this.parseAttr(this.$particles.attr('particles-number-value')),
			      "density": {
			        "enable": this.parseAttr(this.$particles.attr('particles-number-density-enable')),
			        "value_area": this.parseAttr(this.$particles.attr('particles-number-density-value_area')),
			      }
			    },
			    "color": {
			      "value": this.parseAttr(this.$particles.attr('particles-color-value')),
			    },
			    "shape": {
			      "type": this.parseAttr(this.$particles.attr('particles-shape-type')),
			      "stroke": {
			        "width": this.parseAttr(this.$particles.attr('particles-shape-stroke-width')),
			        "color": this.parseAttr(this.$particles.attr('particles-shape-stroke-color')),
			      },
			      "polygon": {
			        "nb_sides": this.parseAttr(this.$particles.attr('particles-shape-polygon-nb_sides')),
			      },
			      "image": {
			        "src": this.parseAttr(this.$particles.attr('particles-shape-image-src')) || '',
			        "width": this.parseAttr(this.$particles.attr('particles-shape-image-width')),
			        "height": this.parseAttr(this.$particles.attr('particles-shape-image-height')),
			      }
			    },
			    "opacity": {
			      "value": this.parseAttr(this.$particles.attr('particles-opacity-value')),
			      "random": this.parseAttr(this.$particles.attr('particles-opacity-random')),
			      "anim": {
			        "enable": this.parseAttr(this.$particles.attr('particles-opacity-anim-enable')),
			        "speed": this.parseAttr(this.$particles.attr('particles-opacity-anim-speed')),
			        "opacity_min": this.parseAttr(this.$particles.attr('particles-opacity-anim-opacity_min')),
			        "sync": this.parseAttr(this.$particles.attr('particles-opacity-anim-sync')),
			      }
			    },
			    "size": {
			      "value": this.parseAttr(this.$particles.attr('particles-size-value')),
			      "random": this.parseAttr(this.$particles.attr('particles-size-random')),
			      "anim": {
			        "enable": this.parseAttr(this.$particles.attr('particles-size-anim-enable')),
			        "speed": this.parseAttr(this.$particles.attr('particles-size-anim-speed')),
			        "size_min": this.parseAttr(this.$particles.attr('particles-size-anim-size_min')),
			        "sync":  this.parseAttr(this.$particles.attr('particles-size-anim-sync')),
			      }
			    },
			    "line_linked": {
			      "enable": this.parseAttr(this.$particles.attr('particles-line_linked-enable')),
			      "distance": this.parseAttr(this.$particles.attr('particles-line_linked-distance')),
			      "color": this.parseAttr(this.$particles.attr('particles-line_linked-color')),
			      "opacity": this.parseAttr(this.$particles.attr('particles-line_linked-opacity')),
			      "width": this.parseAttr(this.$particles.attr('particles-line_linked-witdh')),
			    },
			    "move": {
			      "enable": this.parseAttr(this.$particles.attr('particles-move-enable')),
			      "speed": this.parseAttr(this.$particles.attr('particles-move-speed')),
			      "direction": this.parseAttr(this.$particles.attr('particles-move-direction')),
			      "random": this.parseAttr(this.$particles.attr('particles-move-random')),
			      "straight": this.parseAttr(this.$particles.attr('particles-move-straigth')),
			      "out_mode": this.parseAttr(this.$particles.attr('particles-move-out_mode')),
			      "bounce": this.parseAttr(this.$particles.attr('particles-move-bounce')),
			      "attract": {
			        "enable": this.parseAttr(this.$particles.attr('particles-move-attract-enable')),
			        "rotateX": this.parseAttr(this.$particles.attr('particles-move-attract-rotateX')),
			        "rotateY": this.parseAttr(this.$particles.attr('particles-move-attract-rotateY')),
			      }
			    }
			  },
			  "interactivity": {
			    "detect_on": this.parseAttr(this.$particles.attr('interactivity-detect_on')),
			    "events": {
			      "onhover": {
			        "enable": this.parseAttr(this.$particles.attr('interactivity-events-onhover-enable')),
			        "mode": this.parseAttr(this.$particles.attr('interactivity-events-onhover-mode')),
			      },
			      "onclick": {
			        "enable": this.parseAttr(this.$particles.attr('interactivity-events-onclick-enable')),
			        "mode": this.parseAttr(this.$particles.attr('interactivity-events-onclick-mode')),
			      },
			      "resize": true
			    },
			    "modes": {
			      "grab": {
			        "distance": this.parseAttr(this.$particles.attr('interactivity-modes-grab-distance')),
			        "line_linked": {
			          "opacity": this.parseAttr(this.$particles.attr('interactivity-modes-grab-line_linked-opacity')),
			        }
			      },
			      "bubble": {
			        "distance": this.parseAttr(this.$particles.attr('interactivity-bubble-distance')),
			        "size": this.parseAttr(this.$particles.attr('interactivity-bubble-size')),
			        "duration": this.parseAttr(this.$particles.attr('interactivity-bubble-duration')),
			        "opacity": this.parseAttr(this.$particles.attr('interactivity-bubble-opacity')),
			        "speed": this.parseAttr(this.$particles.attr('interactivity-bubble-speed')),
			      },
			      "repulse": {
			        "distance": this.parseAttr(this.$particles.attr('interactivity-repulse-distance')),
			        "duration": this.parseAttr(this.$particles.attr('interactivity-repulse-duration')),
			      },
			      "push": {
			        "particles_nb": this.parseAttr(this.$particles.attr('interactivity-push-particles_nb')),
			      },
			      "remove": {
			        "particles_nb": this.parseAttr(this.$particles.attr('interactivity-remove-particles_nb')),
			      }
			    }
			  },
			  "retina_detect": this.parseAttr(this.$particles.attr('retina_detect'))
		};
		
		particlesJS(this.$particles.attr('id'), this.model);
    }
});

base.ready().then(function () {
    $('.particles').each(function(index) {
    	(new ParticleSnippet($(this))).create_particles();
    });
    
    if($('#particles-js').length >= 1) {
    	particlesJS.load('particles-js', '/muk_website_snippet_particles/static/assets/particle.json', function() {
		  console.log('callback - particles.js config loaded');
		});
    }
});

return ParticleSnippet;

});


