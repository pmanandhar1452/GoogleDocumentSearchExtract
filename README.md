# GoogleDocumentSearchExtract
Search and extract from google docs document. This is a command line tool that can be used in the following way:

## Usage

`python3 SearchAndExtractFromGDoc.py --id <DocumentID> --token <TokenFile> --secret <ClientSecret> --regex <RegEx> --outfile <OutFile>`

### Parameters

The `DocumentID` is the GUID of the document. `TokenFile` is the name of the token file for access. If the token file does not exist or is invalid, a new one is created. `ClientSecret` is the json secrets file that is generated from the Google API Console.

`RegEx` is the regular expression to search within the document. `OutFile` is the output file which lists the matches in a comma separated value format. The title row
is `|MatchID|MatchText|`. `MatchID` is an integer starting at 1 to the number of matches found.

### Example

The following extracts all emails from the given google document.

`python3 SearchAndExtractFromGDoc.py --id "8736a6176b9c49bb8c8ff5a91a76f779" --token "token.json" --secret "client_secret.json" --regex "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)" --outfile "out.csv"`




