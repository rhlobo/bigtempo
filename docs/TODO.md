TODO
====

Features
- Providers should be able to return date interval data
- Providers should return time pandas series objects

Refactorings
- Data providers should inherit from a RawDataProvider class, subclass of DataProvider, subclass of AbstractProvider
- CotahistProvider should load from bovespa's files, not storing data.

Functional
- Logging


TASKS
=====

- Import cotahist data into existing providers
-- Create update method into providers
-- Test merging and updateing data into providers
- Assure provider data cache is working (implement logging throughout the app)
- Display graph in iPython from imported data
- Create function to detect data errors, splits and joins
-- Measurement by measurement, looking out for 20% + changes
-- Verify if weard changes are persistent or just pontual
- Export splits and joins into a file from my own analysis
- Import splits and joins into a file from yahoo 
- Merge splits and joins files, validating them
- Create provider that provides normalized data
- Create function that correct other data errors
- Create provider that provides corrected data

- Create CSV file containing quotation test data for yahoo
- Test yahoo data
