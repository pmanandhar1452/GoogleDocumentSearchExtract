# GoogleDocumentSearchExtract
Search and extract from google docs document. This is a command line tool that can be used in the following way:

`python3 SearchAndExtractFromGDoc.py --id <DocumentID> --token <TokenFile> --regex <RegEx> --outfile <OutFile>`

The `DocumentID` is the GUID of the document, and the `TokenFile` is the name of the token file for access. If the token file does not exist or is invalid, a new one is created.

`RegEx` is the regular expression to search within the document. `OutFile` is the output file which lists the matches in a comma separated value format. The title row
is `|MatchID|MatchText|`. `MatchID` is an integer starting at 1 to the number of matches found.

