# YouTubeJPtoOJAD
To get the program to work, Line 4: paste the identifier in the URL of the YouTube video (Example for https://www.youtube.com/watch?v=XuxtdiDXcZE, use 'XuxtdiDXcZE') .
The language should be kept as "languages=['ja']" (Line 4)

Firstly, the japanese transcript is obtained from the YouTube webpage. Then, Line 5 to 19 isolates the Japanese text and saves it as a string (This prevents English characters from being sent to OJAD in the next step).

Finally, Line 20 to 40 opens the OJAD webpage and inputs the string in the prompt before submitting the pitch accent request to OJAD.
