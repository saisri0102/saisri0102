enum DateFormat{
    Standard,
    Display
}

// all the optional arguments must be the final arguments

// For example, we cannot make date optional, while making formt mandatory
function formatDate(date : Date , format? : DateFormat){
    
    if(format){
        // .. return formatted date as per required format
    }
    else{
        // return date in a  default format
    }
}

formatDate(new Date()); // second argument which is optional need not be passed
formatDate(new Date(), DateFormat.Standard);

export{}