using Oracle.ManagedDataAccess.Client;
using OracleWebApiTest.Configuration;
using OracleWebApiTest.Models;
using System.Data;
using System.Drawing;

namespace OracleWebApiTest.Repository
{
    public class AlumnosRepository : IAlumnosRepository
    {
        private OracleDBContext _dbContext;
        public AlumnosRepository(OracleDBContext context) { 
            _dbContext = context;
        }

        public List<MateriasDTO> GetMaterias(int idAlumno)
        {
            try
            {
                List<MateriasDTO> result = new List<MateriasDTO>();

                using (OracleConnection connection = new OracleConnection(_dbContext.GetConnectionString))
                {
                    connection.Open();
                    OracleCommand command = new OracleCommand("Lista", connection);
                    command.CommandType = CommandType.StoredProcedure;

                    OracleParameter cursor = new OracleParameter("cursorMemoria", OracleDbType.RefCursor);
                    cursor.Direction = ParameterDirection.Output;
                    command.Parameters.Add(cursor);
                    command.Parameters.Add("p_id_alumno", OracleDbType.Int32).Value = idAlumno; 

                    using (OracleDataReader reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            result.Add(new MateriasDTO                            {
                                NombreAlumno = reader["nombre_alumno"].ToString(),
                                ApellidoAlumno = reader["apellido_alumno"].ToString(),
                                NombreMateria = reader["nombre_materia"].ToString(),
                                Carrera = reader["carrera"].ToString()

                            });
                        }
                    }
                }

                return result;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message );
                return null;
            }

            

        }


    }

}
