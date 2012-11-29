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