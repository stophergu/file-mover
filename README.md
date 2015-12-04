# file-mover
A simple app aimed at pulling photos off SD cards according to date taken and a basic GUI to utilize it

Extensions:
Search for one or more file extensions seperated by a comma(.JPG, .RAW,.txt), spaces can be omitted, search is case sensitive.

From Path or Drive:
Start point for search.  All files matching specified extension(s) will be located in this directory, and all subdirectories contained within it. Last used path or drive will be autofilled

path/to/store/file:
Location to transfer files to. If location folder does not exist, folder will be created.  Last path used will be autofilled.

From Date:
Must follow format of mm/dd/yyyy, if no 'To date' is specified, only 'from date' will be matched.

To Date:
Must follow format of mm/dd/yyyy. If specified, completes range of dates to match files to.

Created/Modified:
Search for files that where created and/or modified within the given date range

