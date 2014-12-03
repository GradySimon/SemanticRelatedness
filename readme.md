# Intro
This project is a tool for calculating the semantic relatedness of two words. As the project stands, it offers an interface that allows you to add words to a Semantic Network and to define connections between those words. You specify the strength of those connections. This project can then provide you with a numeric estimation of the semantic relatedness of any two words in the Semantic Network you have defined.

# Intent
This is one of the first significant (if it counts as such) projects I have done in Python. My goal was to get more comfortable with the language, and to try out a technique I haven't encountered before for measuring semantic relatedness.

The technique I used was to take a graph whose nodes represent words and whose edges represent semantic relationships between words to represent a semantic domain. Each of these edges has a strength associated with it. The project as it stands does not have a way to automatically determine an appropriate strength for a given connection. To calculate the relatedness of two words in the network, the graph is treated as a flow network, and the max flow from the first word to the second word determines relatedness.

This is a slight simplification, since a modified subgraph of the full semantic network is what is actually used in the max flow calculation. See the doc strings in relatedness.py for more detail.

# Projects and Resources Used

[NetworkX](http://networkx.lanl.gov/index.html) - An excellent graph  package for Python. I used NetworkX undirected graphs as the underlying data structure for my Semantic_Network class. NetworkX did some of the heavy lifting, particularly for the max flow calculation. I highly recommend NetworkX for doing graph work in Python.

[Matplotlib](http://matplotlib.sourceforge.net/) - A 2D plotting library for python. It's not actually used in the core of my project, but it is used in the testing module, and its visualizations definitely helped during the development process.

[lxml](http://lxml.de/) - An XML/HTML parser for Python. I used this to extract the content from the XML document that Wikipedia's API returns in the Wikipedia sample driver I wrote for the project.

[Wikipedia](http://www.wikipedia.org/) - I wrote a Wikipedia driver for the project that allows you to demo the relatedness calculation. This was also enormously helpful during the development process. This driver uses the Wikipedia API to pull the introduction sections from Wikipedia articles and parses out the links contained as a basis for building a semantic network. A big thanks to the Wikipedia team and all of the people who make Wikipedia the amazing resource that it is.

# License

[MIT License](http://opensource.org/licenses/MIT)

Copyright (c) 2012 Grady Simon

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
