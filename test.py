import config
import testconnection as tc

MyClient = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", config.password,
                         api_key="5eb00202-3701-47ca-9bda-317e209b29ee")

MyClient2 = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", api_key="5eb00202-3701-47ca-9bda-317e209b29ee")
MyClient3 = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", config.password)

FailingClient = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk",
                              api_key="5eb00202-3701-47ca-9bda-317e209b29ee")


# print(MyClient.properties("folders","3b3ca080-0c75-4a50-a993-5ec6e87f631e").json())
