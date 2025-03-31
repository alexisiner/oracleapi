namespace OracleWebApiTest.Configuration
{
    public class OracleDBContext
    {
        private readonly string _ConnectionString;
        public OracleDBContext(IConfiguration configuration) {

            _ConnectionString = configuration.GetConnectionString("OracleDBConnectionstring");
        
        }

        public string GetConnectionString { get { return _ConnectionString; } }
    }
}
