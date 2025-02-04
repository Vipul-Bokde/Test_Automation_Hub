mvn clean test -Dsurefire.suiteXmlFiles=smoke_suite.xml -Dgroups=smoke
mvn clean test -Dsurefire.suiteXmlFiles=sanity_suite.xml -Dgroups=sanity



(no space after comma)
mvn clean test -Dsurefire.suiteXmlFiles=smoke_suite.xml -Dgroups=smoke,sanity

Explanation:
-Dsurefire.suiteXmlFiles=smoke_suite.xml → Runs the specific TestNG suite file.
-Dgroups=smoke,sanity → Executes only test cases tagged with @Test(groups={"smoke", "sanity"}).

 
mvn clean test -Dsurefire.suiteXmlFiles=smoke_suite.xml,sanity_suite.xml


multiple xml at same time
