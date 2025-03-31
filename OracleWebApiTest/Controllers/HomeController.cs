using Microsoft.AspNetCore.Mvc;
using OracleWebApiTest.Repository;

namespace OracleWebApiTest.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class HomeController : Controller
    {
        IAlumnosRepository _alumnosRepository;
        public HomeController(IAlumnosRepository alumnosRepository) { 

            _alumnosRepository = alumnosRepository;
        
        } 
        [HttpGet("Index/{idAlumno}")]
        public IActionResult Index(int idAlumno)
        {
            return Ok(_alumnosRepository.GetMaterias(idAlumno));
        }
    }
}
