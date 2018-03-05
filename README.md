# HOA_Market_Analysis
Programs to automate the collection and curation of data pertaining to homeowners associations.

Product Backlog for CompsHOA.py:
* Add number formatting
    * SF: Add comma for every third digit
    * Sale Price: $
    * Price/SF: $
    * Zestimate: $
    * Zestimate/SF: $
    * Prev Sale Price: $
    * Appreciation: %
* Auto resize the columns
* More data:
    * Recently sold comps nearby

Notes on Development Process:

Making the program work as desired was actually fairly straight forward. Getting data from the Zillow API and then using loops to write that data into an Excel file with OpenPyXL was fairly easy, especially since I had experience with OpenPyXL. I was able to get the program to do what I wanted. The problem was the Zillow API gave me data that wasn’t precisely relevant to my real-world application.

To solve this problem I had to find another API that would give me property data more relevant to my use. I found the Onboard developer API that didn’t give exact comparables for a given property but did have an API that gave ALL the properties within a certain distance of a given property. This is less elegant but much better suited to my purposes.

Commenting my code and ordering the code the way I did really helped me come back to it a few weeks later and tell what was happening.

Onboard, unlike Zillow, also has historical sales data for each property, which is data I can use to fill out the Excel document.

I then ran into a problem with the Onboard API. The way I collected the data and stored it in a Python dictionary was not conducive to the way the API gives data if there’s a property with no sales history. To solve this exception I also couldn’t just throw in a “try” and “except” or an “if” statement to solve the outlier. This is because I still need the property’s characteristics, even if there’s no sales history, and both these data sets were being retrieved from the same API.

The structural problem is that I’m defining functions. I used functions that would only be used once because I wanted to keep my code easily readable and testable for myself. I wanted the code to be more segmented than it otherwise would be.
