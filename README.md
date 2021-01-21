# promote_grant_changes.py

This is a script that I use to help organize documents submitted to administrators and collaborators when writing grants. 

It looks for grant documents (identified by a tracking prefix). When a prefixed file is found, it's copied to the target directory if the file hasn't been seen before.  If the file has been seen before, the file hash is checked. If the hash has changed, the file is copied to the target directory. All copied files have a time-stamp suffix added to differentiate versions. There are several assumptions.

* The python script is stored one level down from the grant documents. I store it in an 'info' directory.
* In the same directory as the python script, there is a file named 'rms_doc_num.txt'. It contains only a single line: the tracking ID assigned to the application in the Research Management System (RMS). In this case I'm using 'XXXXXX' as a dummy ID.
* Grant documents are prefixed by the ID.
* There is a target folder for grant documents to be copied to.

Could the RMS ID be passed as an argument? Yes. Could the document holding an RMS ID be dynamically named and passed as an argument? Yes. Could the source directory be an arument? Also yes.

But I use the same layout every time and this works. YMMV. ¯\\_(ツ)_/¯

## Example folder layout
    .
    ├── info
	│   ├── rms_doc_num.txt
	│   └── promote_grant_changes.py
	├── send_to_admins
    ├── XXXXXX_FileA.docx
    └── XXXXXX_FileB.xlsx
	
## Example usage with recommended layout

### Dry run
```bash
python promote_grant_changes.py --dryrun ../send_to_admins
```

### Normal
```bash
python promote_grant_changes.py ../send_to_admins
```
