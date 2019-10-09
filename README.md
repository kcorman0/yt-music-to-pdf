# PDF Sheet Music Generator

There are many YouTube videos that scroll through sheet music but do not provide a PDF, or have it behind a paywall. As someone who has ran into this problem many times, I created this project to turned these videos into PDFs for free. 

## How it works

After trying a variety of different vision processing methods, it seems that searching for a specific color in a HSV space is the most reliable method (as there is almost always a colored bar that moves through the music). 
Whenever there is a large jump in the bar's X value, the program will assume it has moved on to the next line of music and will take a screenshot of the new line. At the end, all of the screenshots will be compiled into a PDF using FPDF.

## Examples

I created a simple web interface with Flask that prompts the user for a YouTube URL, and the color to filter for:

![Web](https://raw.githubusercontent.com/kcorman0/yt-music-to-pdf/master/images/web.png)

Below is an example of HSV filtering:

![Web](https://raw.githubusercontent.com/kcorman0/yt-music-to-pdf/master/images/filtered.png)

Final PDF (bottom doesn't cut off in actual PDF): 

![Final](https://raw.githubusercontent.com/kcorman0/yt-music-to-pdf/master/images/example_pdf.png)