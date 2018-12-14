# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 16:30:41 2018

@author: dongyu
"""

import pdb

class GoogleMapHeatmap(object):
    
    def __init__(self, center_lat, center_lng, zoom, apikey='',  **kwargs):
        
        self.__dict__.update(kwargs)
        
        self.center = (float(center_lat), float(center_lng))
        self.zoom = int(zoom)
        self.apikey = str(apikey)
        
        self.heatmap_points = []
        
        
    def heatmap(self, lats, lngs, gradient=None, maxIntensity=0.2, dissipating=True):
        """
        :param lats: list of latitudes
        :param lngs: list of longitudes
        :param maxIntensity:(int) max frequency to use when plotting. Default (None) uses max value on map domain.
        :param threshold:
        :param radius: The hardest param. Example (string):
        :return:
        """
        self.maxIntensity = maxIntensity        
        
        settings = {}
        # Try to give anyone using threshold a heads up.
#        settings['radius'] = radius
        settings['gradient'] = gradient
#        settings['opacity'] = opacity
        settings['maxIntensity'] = self.maxIntensity
        settings['dissipating'] = dissipating
        settings = self._process_heatmap_kwargs(settings)

        heatmap_points = []
        for lat, lng in zip(lats, lngs):
            heatmap_points.append((lat, lng))
        self.heatmap_points.append((heatmap_points, settings))
        
        #pdb.set_trace()
        
        
        
    def _process_heatmap_kwargs(self, settings_dict):
        settings_string = ''
#        settings_string += "heatmap.set('radius', %d);\n" % settings_dict['radius']
        settings_string += "heatmap.set('maxIntensity', %f);\n" % settings_dict['maxIntensity']
#        settings_string += "heatmap.set('opacity', %f);\n" % settings_dict['opacity']

        dissipation_string = 'true' if settings_dict['dissipating'] else 'false'
        settings_string += "heatmap.set('dissipating', %s);\n" % (dissipation_string)

        gradient = settings_dict['gradient']
        if gradient:
            gradient_string = "var gradient = [\n"
            for r, g, b, a in gradient:
                gradient_string += "\t" + "'rgba(%d, %d, %d, %d)',\n" % (r, g, b, a)
            gradient_string += '];' + '\n'
            gradient_string += "heatmap.set('gradient', gradient);\n"

            settings_string += gradient_string

        return settings_string
        
    def draw(self, htmlfile):
        """Create the html file which include one google map and all points and paths. If 
        no string is provided, return the raw html.
        """
        f = open(htmlfile, 'w')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write(
            '<meta charset="utf-8">\n')
        f.write(
            '<title>Heatmaps</title>\n')
        f.write(
            '<script type="text/javascript" src="https://code.jquery.com/jquery-compat-git.js"></script>\n')
        f.write(
            '<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=places,visualization&amp;sensor=false"></script>\n')
        f.write(
            '<style type="text/css">\n')
        f.write(
            '* {box-sizing: border-box;}\n')
        f.write(
            '#map {height: 100%;}\n')            
        f.write(
            'html,body {height: 100%;margin: 0;padding: 0;}\n')
        f.write(
            "#floating-panel {position: absolute;top: 10px;left: 25%;z-index: 5;background-color: #fff;padding: 5px;border: 1px solid #999;text-align: center;font-family: 'Roboto', 'sans-serif';line-height: 30px;padding-left: 10px;}\n")
        f.write(
            '#floating-panel {background-color: #fff;border: 1px solid #999;left: 1%;padding: 5px;position: absolute;top: 40px;z-index: 5;}\n')
        f.write(
            '#legend {position: relative;width: 650px;height: 30px;margin-top: 10px;}\n')
        f.write(
            '#legendGradient {width: 100%;height: 15px;border: 1px solid black;}\n')
        f.write(
            '</style>\n')
        f.write('</head>\n')
        
        f.write('<body>\n')
        f.write(
            '<div id="floating-panel">\n')
        f.write(
            '<button onclick="toggleHeatmap()">Toggle Heatmap</button>\n')
        f.write(
            '<button onclick="changeRadius()">Change radius</button>\n')
        f.write(
            '<button onclick="changeOpacity()">Change opacity</button>\n')
        f.write('</div>\n')
        f.write('<div id="map"></div>\n')
        f.write(
            '<div id="legend">\n')
        f.write(
            '<div id="legendGradient"></div>\n')
        f.write('</div>\n')
        f.write('<script type="text/javascript">\n')
        
        f.write('var map, heatmap, gradient;\n')   
        #f.write('var map, gradient;\n')             
        
        f.write('\tfunction initialize() {\n')
        self.write_map(f)
        self.write_heatmap(f)        
        f.write('}\n')
        
        ## functions
        f.write('function toggleHeatmap() {heatmap.setMap(heatmap.getMap() ? null : map);}\n')
        f.write("function changeRadius() {heatmap.set('radius', heatmap.get('radius') ? null : 20);}\n")
        f.write("function changeOpacity() {heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);}\n")
        
        ## heatmap setGradient()
        self.write_setGradient(f)
        ## setLegendGradient()
        self.write_setLegendGradient(f)
        ## setLegendLabels()
        self.write_setLegendLabels(f)
        
        f.write("google.maps.event.addDomListener(window, 'load', initialize);\n")
        f.write('</script>\n')
        f.write('</body>\n')
        f.write('</html>\n')
        f.close()
   
     
    def write_map(self,  f):
        f.write(
            '\t\t map = new google.maps.Map(document.getElementById("map"), {\n')
        f.write('\t\t\tzoom: %d,\n' % (self.zoom))
        f.write('\t\t\tcenter: {\n')
        f.write('\t\t\tlat: %f,\n'%self.center[0])
        f.write('\t\t\tlng: %f \n'%self.center[1])
        f.write('\t\t\t},\n')
        f.write("\t\t\t mapTypeId: 'satellite' \n")
        f.write('\t\t\t});\n')
        f.write('\n')
        
        
    
    def write_heatmap(self, f):
        for heatmap_points, settings_string in self.heatmap_points:
            f.write('var heatmap_points = [\n')
            for heatmap_lat, heatmap_lng in heatmap_points:
                f.write('new google.maps.LatLng(%f, %f),\n' %
                        (heatmap_lat, heatmap_lng))
            f.write('];\n')
            f.write('\n')
            f.write('var pointArray = new google.maps.MVCArray(heatmap_points);' + '\n')
            #f.write('var heatmap;' + '\n')
            f.write('heatmap = new google.maps.visualization.HeatmapLayer({' + '\n')
            f.write('\n')
            f.write('data: pointArray' + '\n')
            f.write('});' + '\n')
            f.write('heatmap.setMap(map);' + '\n')
            f.write(settings_string)
        
        f.write('setGradient();\n')
        f.write('setLegendGradient();\n')
        f.write('setLegendLabels();\n')
        
        
    def write_setGradient(self, f):
        
        f.write('function setGradient() {\n')
        f.write('gradient = ["rgba(102, 255, 0, 0)",\n')
        f.write('"rgba(102, 255, 0, 1)",\n')
        f.write('"rgba(147, 255, 0, 1)",\n')
        f.write('"rgba(193, 255, 0, 1)",\n')
        f.write('"rgba(238, 255, 0, 1)",\n')
        f.write('"rgba(244, 227, 0, 1)",\n')
        f.write('"rgba(249, 198, 0, 1)",\n')
        f.write('"rgba(255, 170, 0, 1)",\n')
        f.write('"rgba(255, 113, 0, 1)",\n')
        f.write('"rgba(255, 57, 0, 1)",\n')
        f.write('"rgba(255, 0, 0, 1)"]\n')
        f.write("heatmap.set('gradient', gradient);\n")
        f.write('}\n')
        
    def write_setLegendGradient(self,f):
        
        f.write('function setLegendGradient() {\n')
        f.write("var gradientCss = '(left';\n")
        f.write('for (var i = 0; i < gradient.length; ++i) {\n')
        f.write("gradientCss += ', ' + gradient[i];\n")
        f.write('}\n')
        f.write("gradientCss += ')';\n")
        f.write('\n')
        f.write("$('#legendGradient').css('background', '-webkit-linear-gradient' + gradientCss);\n")
        f.write("$('#legendGradient').css('background', '-moz-linear-gradient' + gradientCss);\n")
        f.write("$('#legendGradient').css('background', '-o-linear-gradient' + gradientCss);\n")
        f.write("$('#legendGradient').css('background', 'linear-gradient' + gradientCss);\n")
        f.write('}\n')
        
    def write_setLegendLabels(self,f):
        
        f.write('function setLegendLabels() {\n')
        f.write("google.maps.event.addListenerOnce(map, 'tilesloaded', function() {\n")
        f.write('var maxIntensity = %f*25;\n'%self.maxIntensity)
        f.write("var legendWidth = $('#legendGradient').outerWidth();\n")
        f.write('\n')
        f.write('for (var i = 0; i <= maxIntensity; ++i) {\n')
        f.write('var offset = i * legendWidth / maxIntensity;\n')
        f.write('if (i > 0 && i < maxIntensity) {\n')
        f.write('offset -= 0.5;\n')        
        f.write('} else if (i == maxIntensity) {\n')
        f.write('offset -= 1;\n')
        f.write('}\n')
        f.write("$('#legend').append($('<div>').css({\n")
        f.write("'position': 'absolute',\n")
        f.write("'left': offset + 'px',\n")
        f.write("'top': '15px',\n")
        f.write("'width': '1px',\n")
        f.write("'height': '3px',\n")
        f.write("'background': 'black'\n")
        f.write("}));\n")
        f.write("$('#legend').append($('<div>').css({\n")
        f.write("'position': 'absolute',\n")
        f.write("'left': (offset - 5) + 'px',\n")
        f.write("'top': '18px',\n")
        f.write("'width': '10px',\n")
        f.write("'text-align': 'center',\n")
        f.write("'font-size': '0.8em',\n")
        f.write("}).html(i/25));\n")
        f.write('}\n')
        f.write('});\n')
        f.write('}\n')

        
        
        
        
        
            
            
