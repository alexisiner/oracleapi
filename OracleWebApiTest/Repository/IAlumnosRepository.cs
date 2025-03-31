using OracleWebApiTest.Models;

namespace OracleWebApiTest.Repository
{
    public interface IAlumnosRepository
    {
        //aqui van los metodos
        public List<MateriasDTO> GetMaterias(int idAlumno);
    }
}
