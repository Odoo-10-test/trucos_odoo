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

odoo.define('muk_website_snippet_particles.editor', function (require) {
'use strict';

var widget = require('web_editor.widget');
var s_options = require('web_editor.snippets.options');
var particles = require('muk_website_snippet_particles.frontend');

s_options.registry.snippet_particles_options = s_options.Class.extend({
    start: function () {
        this._super.apply(this, arguments);
        
        var self = this;
        
        this.$particles = this.$target.find('.particles');
        this.$particles.attr('id', 'particles' + _.uniqueId());

        this.snippet = new particles(this.$particles);
        this.snippet.create_particles();
        
        var $toggles = this.$el.find('.muk_particle_section_menu');
        var $tabs = this.$el.find('.muk_particle_section_tabs');
        var $sections = $tabs.find('.muk_particle_section');
        
        $sections.each(function () {
            var $section = $(this);
            var id = 'muk_particle_' + $section.data('name') + _.uniqueId();
            var $li = $('<li/>').append($('<a/>', {href: '#' + id})
                        .append($('<i/>', {'class': $section.data('iconClass') || ''})));
            $toggles.append($li);
            $tabs.append($section.attr('id', id));
        });

        $tabs.find('div').first().addClass('active');
        $toggles.find('li').first().addClass('active');
        $toggles.on('click mouseover', '> li > a', function (e) {
            e.preventDefault();
            e.stopPropagation();
            $(this).tab('show');
        });
        
        this.$el.find('.muk_checkbox-opt').each(function () {
        	var $area = $(this);
        	var id = 'muk_particles_checkbox' + _.uniqueId();
        	$area.find('.muk_particles-checkbox').attr('id', id);
        	$area.find('.muk_particles-checkbox-label').attr('for', id);
        });
        
        this.$el.find('.muk_particles-slider').on('click change mousedown mousemove', function(e) {
            e.stopPropagation();
            $(e.currentTarget).parent().find('.muk_particles-slider-value').text($(this).val());
        });
        this.$el.find('.muk_particles-checkbox-label').on('click change mousedown mousemove', function(e) {
            e.stopPropagation();
            if(e.type === 'click') {
            	var checkbox = $(e.currentTarget).parent().find('.muk_particles-checkbox');
            	checkbox.checked = !checkbox.checked;
            }
        });
        this.$el.find('.muk_particles-checkbox').on('click change', function(e) {
            e.stopPropagation();
        });
        this.$el.find('.muk_particles-color-picker').on('click change mousedown mousemove', function(e) {
            e.stopPropagation();
            $(e.currentTarget).parent().find('.muk_particles-color-picker-value').text($(this).val());
        });
        this.$el.find('.muk_particles-image-button').on('click change mousedown mousemove', function(e) {
            e.stopPropagation();
        });
        this.$el.find('.muk_particles-select').on('click change mousedown mousemove', function(e) {
            e.stopPropagation();
        });

        this.setUpSlider('.muk_particles-number-value', 'particles-number-value');
        this.setUpCheckbox('.muk_particles-number-density-enable', 'particles-number-density-enable');
        this.setUpSlider('.muk_particles-number-density-value_area', 'particles-number-density-value_area');
        this.setUpColor('.muk_particles-color-value', 'particles-color-value');
        this.setUpSlider('.muk_particles-shape-stroke-width', 'particles-shape-stroke-width');
        this.setUpColor('.muk_particles-shape-stroke-color', 'particles-shape-stroke-color');
        this.setUpSlider('.muk_particles-shape-polygon-nb_sides', 'particles-shape-polygon-nb_sides');
        this.setUpImageSelect('.muk_particles-shape-image-src', 'particles-shape-image-src');
        this.setUpSlider('.muk_particles-shape-image-width', 'particles-shape-image-width');
        this.setUpSlider('.muk_particles-shape-image-height', 'particles-shape-image-height');
        this.setUpSelection('.muk_particles-shape-type', 'particles-shape-type');
        this.setUpCheckbox('.muk_particles-size-anim-enable', 'particles-size-anim-enable');
        this.setUpSlider('.muk_particles-size-anim-speed', 'particles-size-anim-speed');
        this.setUpSlider('.muk_particles-size-anim-size_min', 'particles-size-anim-size_min');
        this.setUpCheckbox('.muk_particles-size-anim-sync', 'particles-size-anim-sync');
        this.setUpSlider('.muk_particles-size-value', 'particles-size-value');
        this.setUpCheckbox('.muk_particles-size-random', 'particles-size-random');
        this.setUpCheckbox('.muk_particles-opacity-anim-enable', 'particles-opacity-anim-enable');
        this.setUpSlider('.muk_particles-opacity-anim-speed', 'particles-opacity-anim-speed');
        this.setUpSlider('.muk_particles-opacity-anim-size_min', 'particles-opacity-anim-size_min');
        this.setUpCheckbox('.muk_particles-opacity-anim-sync', 'particles-opacity-anim-sync');
        this.setUpSlider('.muk_particles-opacity-value', 'particles-opacity-value');
        this.setUpCheckbox('.muk_particles-opacity-random', 'particles-opacity-random');
        this.setUpCheckbox('.muk_particles-line_linked-enable', 'particles-line_linked-enable');
        this.setUpSlider('.muk_particles-line_linked-distance', 'particles-line_linked-distance');
        this.setUpColor('.muk_particles-line_linked-color', 'particles-line_linked-color');
        this.setUpSlider('.muk_particles-line_linked-opacity', 'particles-line_linked-opacity');
        this.setUpSlider('.muk_particles-line_linked-witdh', 'particles-line_linked-witdh');
        this.setUpCheckbox('.muk_particles-move-enable', 'particles-move-enable');
        this.setUpSelection('.muk_particles-move-direction', 'particles-move-direction');
        this.setUpCheckbox('.muk_particles-move-random', 'particles-move-random');
        this.setUpCheckbox('.muk_particles-move-straigth', 'particles-move-straigth');
        this.setUpSlider('.muk_particles-move-speed', 'particles-move-speed');
        this.setUpSelection('.muk_particles-move-out_mode', 'particles-move-out_mode');
        this.setUpCheckbox('.muk_particles-move-attract-enable', 'particles-move-attract-enable');
        this.setUpSlider('.muk_particles-move-attract-rotateX', 'particles-move-attract-rotateX');
        this.setUpSlider('.muk_particles-move-attract-rotateY', 'particles-move-attract-rotateY');
        this.setUpCheckbox('.muk_interactivity-events-onhover-enable', 'interactivity-events-onhover-enable');
        this.setUpSelection('.muk_interactivity-events-onhover-mode', 'interactivity-events-onhover-mode');
        this.setUpCheckbox('.muk_interactivity-events-onclick-enable', 'interactivity-events-onclick-enable');
        this.setUpSelection('.muk_interactivity-events-onclick-mode', 'interactivity-events-onclick-mode');
        this.setUpSelection('.muk_interactivity-detect_on', 'interactivity-detect_on');
        this.setUpCheckbox('.muk_muk_retina_detect', 'muk_retina_detect');
        this.setUpSlider('.muk_interactivity-modes-grab-distance', 'interactivity-modes-grab-distance');
        this.setUpSlider('.muk_interactivity-modes-grab-line_linked-opacity', 'interactivity-modes-grab-line_linked-opacity');
        this.setUpSlider('.muk_interactivity-bubble-distance', 'interactivity-bubble-distance');
        this.setUpSlider('.muk_interactivity-bubble-size', 'interactivity-bubble-size');
        this.setUpSlider('.muk_interactivity-bubble-duration', 'interactivity-bubble-duration');
        this.setUpSlider('.muk_interactivity-bubble-opacity', 'interactivity-bubble-opacity');
        this.setUpSlider('.muk_interactivity-bubble-speed', 'interactivity-bubble-speed');
        this.setUpSlider('.muk_interactivity-repulse-distance', 'interactivity-repulse-distance');
        this.setUpSlider('.muk_interactivity-repulse-duration', 'interactivity-repulse-duration');
        this.setUpSlider('.interactivity-push-particles_nb', 'interactivity-push-particles_nb');
        this.setUpSlider('.interactivity-remove-particles_nb', 'interactivity-remove-particles_nb');
    },
    setUpSelection: function($selector, attribute) {
    	var self = this;
    	this.$el.find($selector).on('change', function(e) {
    		self.$particles.attr(attribute, this.value);
            self.$target.closest(".o_editable").trigger("content_changed");
            self.snippet.create_particles();
    	});
    	this.$el.find($selector).val(this.$particles.attr(attribute));
    },
    setUpImageSelect: function($selector, attribute) {
    	var self = this;
    	this.$el.find($selector + '-delete').on('click', function(e) {
    		self.$particles.attr(attribute, "");
            self.$target.closest(".o_editable").trigger("content_changed");
            self.snippet.create_particles();
    	});
    	this.$el.find($selector).on('click', function(e) {
    		var $image = $("<img/>", {"class": "hidden", "src": ""}).appendTo(self.$target);
        	var _editor = new widget.MediaDialog(null, {}, null, $image[0]).open();
            _editor.$('[href="#editor-media-video"], [href="#editor-media-icon"]').addClass('hidden');

            _editor.on('save', self, function () {
                self.$particles.attr(attribute, $image.attr("src"));            
                self.$target.closest(".o_editable").trigger("content_changed");
                self.snippet.create_particles();
            });
            _editor.on('closed', self, function () {
            	$image.remove();
            });
    	});
    },
    setUpCheckbox: function($selector, attribute) {
    	var self = this;
    	this.$el.find($selector).on('change', function(e) {
            self.$particles.attr(attribute, $(this).checked);
            self.$target.closest(".o_editable").trigger("content_changed");
            self.snippet.create_particles();
        });
    	if(this.$particles.attr(attribute) === 'true') {
            this.$el.find($selector).attr('checked', this.$particles.attr(attribute));
    	}
    },
    setUpSlider: function($selector, attribute) {
    	var self = this;
    	this.$el.find($selector).on('change', function(e) {
            self.$particles.attr(attribute, $(this).val());
            self.$target.closest(".o_editable").trigger("content_changed");
            self.snippet.create_particles();
        });
        this.$el.find($selector).val(this.$particles.attr(attribute));
        this.$el.find($selector).trigger('change');
    },
    setUpColor: function($selector, attribute) {
    	var self = this;
    	this.$el.find($selector).on('change', function(e) {
            self.$particles.attr(attribute, $(this).val());
            self.$target.closest(".o_editable").trigger("content_changed");
            self.snippet.create_particles();
        });
        this.$el.find($selector).val(this.$particles.attr(attribute));
        this.$el.find($selector).trigger('change');
    }
});

});
   
