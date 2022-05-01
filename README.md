# Open Target Association Data loader Analytics Tool - Python
A data laoder tool built in python
    - Loading data from FTP server
    - Parsing and performing the data calcualtions

## Steps to Run
    From the project root directory execute below commands
    - make bootstrap
        - Install the modules needed
    - make test
        - Run the test cases for the data calculations
    - make start
        - start the application
        1. Parse each evidence object and the `diseaseId`, `targetId`, and `score` fields.
        2. For each `targetId` and `diseaseId` pair, calculating the median and 3 greatest unique `score` values.
        3. Joined the targets and diseases datasets on the `targetId` = `target.id` and `diseaseId` = `disease.id` fields.
        4. Aded the `target.approvedSymbol` and `disease.name` fields to the table
        5. Output - <project-root-dir>.result.json
            Resultant table in JSON format, sorted in ascending order by the median value of the `score`.
        6. Logs the number of target pair count having relationship with at least 2 diseases.
    
## Future Scope and Trade Offs

    - FTP host , evidence, target and disease dir locations can be configurable using a config.json
    - Can write test cases for the FTP data loader part - Right now concentrate mainly on the open target service functionalities.
    - Can make the individual json dowloads also concurrent.
    - Currently downloading all the data jsons to a single folder, had issues with keeping that in different folders to run concurrently.

## Notes
    - First attempt in python data loading