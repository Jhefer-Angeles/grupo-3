using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using ProductosBreeze1.Models;

namespace ProductosBreeze1.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
namespace ProductosBreeze1.Controllers
{
    [Authorize(Roles = "Admin,Empleado")]
    public class InventarioController : Controller
    {
        private readonly AppDbContext _context;

        public InventarioController(AppDbContext context)
        {
            _context = context;
        }


        // 1. MENÚ PRINCIPAL
        public async Task<IActionResult> Menu()
        {
            ViewBag.TotalProductos = await _context.Productos.CountAsync();
            ViewBag.BajoStock = await _context.Productos.CountAsync(p => p.Stock < 5);
            ViewBag.VentasHoy = await _context.Ventas.Where(v => v.FechaHora.Date == DateTime.Today).CountAsync();
            return View();
        }

        // 2. REGISTRAR PRODUCTO (Solo Admin)
        [Authorize(Roles = "Admin")]
        public IActionResult RegistrarProducto() => View();

        [HttpPost]
        [Authorize(Roles = "Admin")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> RegistrarProducto(Producto producto)
        {
            if (ModelState.IsValid)
            {
                _context.Add(producto);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(MostrarProductos));
            }
            return View(producto);
        }

        // 3. INGRESAR STOCK
        public async Task<IActionResult> IngresarStock()
        {
            ViewBag.Productos = await _context.Productos.ToListAsync();
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> IngresarStock(int productoId, int cantidad)
        {
            var producto = await _context.Productos.FindAsync(productoId);
            if (producto != null && cantidad > 0)
            {
                producto.Stock += cantidad;

                var historial = new HistorialIngreso
                {
                    Empleado = User.Identity.Name ?? "Empleado",
                    ProductoId = productoId,
                    Cantidad = cantidad,
                    FechaHora = DateTime.Now
                };

                _context.Add(historial);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(MostrarProductos));
            }
            return RedirectToAction(nameof(IngresarStock));
        }

        // 4. SALIDA DE STOCK / VENTA
        public async Task<IActionResult> SalidaStock()
        {
            ViewBag.Productos = await _context.Productos.Where(p => p.Stock > 0).ToListAsync();
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> RegistrarVenta(string cliente, string metodoPago, int[] productoIds, int[] cantidades)
        {
            if (string.IsNullOrEmpty(cliente) || productoIds == null || productoIds.Length == 0)
            {
                return RedirectToAction(nameof(SalidaStock));
            }

            var venta = new Venta
            {
                Cliente = cliente,
                MetodoPago = metodoPago,
                Empleado = User.Identity.Name ?? "Empleado",
                FechaHora = DateTime.Now,
                Total = 0
            };

            decimal totalVenta = 0;

            for (int i = 0; i < productoIds.Length; i++)
            {
                int pId = productoIds[i];
                int cant = cantidades[i];

                var prod = await _context.Productos.FindAsync(pId);
                if (prod != null && prod.Stock >= cant && cant > 0)
                {
                    prod.Stock -= cant;
                    var detalle = new DetalleVenta
                    {
                        ProductoId = pId,
                        Cantidad = cant,
                        PrecioUnitario = prod.Precio
                    };
                    venta.Detalles.Add(detalle);
                    totalVenta += prod.Precio * cant;
                }
            }

            if (venta.Detalles.Count > 0)
            {
                venta.Total = totalVenta;
                _context.Add(venta);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Comprobante), new { id = venta.Id });
            }

            return RedirectToAction(nameof(SalidaStock));
        }

        // COMPROBANTE DE PAGO
        public async Task<IActionResult> Comprobante(int id)
        {
            var venta = await _context.Ventas
                .Include(v => v.Detalles)
                .ThenInclude(d => d.Producto)
                .FirstOrDefaultAsync(v => v.Id == id);

            if (venta == null) return NotFound();
            return View(venta);
        }

        // 5 & 6. MOSTRAR TODOS LOS PRODUCTOS Y BUSCAR
        public async Task<IActionResult> MostrarProductos(string buscar)
        {
            var productos = from p in _context.Productos select p;

            if (!string.IsNullOrEmpty(buscar))
            {
                productos = productos.Where(p => p.Nombre.ToLower().Contains(buscar.ToLower()));
            }

            ViewBag.Busqueda = buscar;
            return View(await productos.ToListAsync());
        }

        // EDITAR (Solo Admin)
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Editar(int id)
        {
            var producto = await _context.Productos.FindAsync(id);
            if (producto == null) return NotFound();
            return View(producto);
        }

        [HttpPost]
        [Authorize(Roles = "Admin")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Editar(Producto producto)
        {
            if (ModelState.IsValid)
            {
                _context.Update(producto);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(MostrarProductos));
            }
            return View(producto);
        }

        // ELIMINAR (Solo Admin)
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Eliminar(int id)
        {
            var producto = await _context.Productos.FindAsync(id);
            if (producto != null)
            {
                _context.Productos.Remove(producto);
                await _context.SaveChangesAsync();
            }
            return RedirectToAction(nameof(MostrarProductos));
        }

        // 7. ALERTAS DE STOCK
        public async Task<IActionResult> AlertasStock()
        {
            var productos = await _context.Productos.ToListAsync();
            return View(productos);
        }

        // 8. HISTORIAL DE INGRESOS
        public async Task<IActionResult> HistorialIngresos()
        {
            var historial = await _context.HistorialIngresos.Include(h => h.Producto).OrderByDescending(h => h.FechaHora).ToListAsync();
            return View(historial);
        }

        // 9. HISTORIAL DE VENTAS
        public async Task<IActionResult> HistorialVentas()
        {
            var ventas = await _context.Ventas.OrderByDescending(v => v.FechaHora).ToListAsync();
            return View(ventas);
        }
    }
}
namespace ProductosBreeze1.Controllers
{
    public class LoginController : Controller
    {
        private readonly AppDbContext _dbconext;

        public LoginController(AppDbContext dbcontext)
        {
            _dbconext = dbcontext;
        }

        [HttpGet]
        public IActionResult Registro()
        {
            ViewBag.Roles = _dbconext.Roles.ToList();
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Registro(UserVM model)
        {
            if (model.Pass != model.RepPass)
            {
                ViewData["Mensaje"] = "Las contraseñas no coinciden";
                ViewBag.Roles = _dbconext.Roles.ToList();
                return View();
            }

            Usuario usuario = new Usuario()
            {
                NameUser = model.Name,
                Email = model.Email,
                Password = model.Pass,
                RolId = model.IdRol
            };

            await _dbconext.Usuarios.AddAsync(usuario);
            await _dbconext.SaveChangesAsync();

            if (usuario.idUsuario != 0) return RedirectToAction("Login", "Login");

            ViewData["Mensaje"] = "El usuario no pudo crearse";
            ViewBag.Roles = _dbconext.Roles.ToList();
            return View();
        }

        [HttpGet]
        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Login(LoginVM model)
        {
            // Buscamos el usuario incluyendo los datos de su tabla de Roles vinculada
            Usuario? usuario_encontrado = await _dbconext.Usuarios
                .Include(u => u.Roles)
                .Where(u => u.Email == model.Email && u.Password == model.Password)
                .FirstOrDefaultAsync();

            if (usuario_encontrado == null)
            {
                ViewData["Mensaje"] = "No se encontraron usuarios";
                return View();
            }

            // ==========================================
            // 🔐 CONSTRUCCIÓN DE LA COOKIE DE AUTENTICACIÓN
            // ==========================================
            var claims = new List<Claim>
            {
                // Guardamos el nombre de usuario y su Rol para que el _Layout lo lea automáticamente
                new Claim(ClaimTypes.Name, usuario_encontrado.NameUser),
                new Claim(ClaimTypes.Role, usuario_encontrado.Roles.Nombre)
            };

            var claimsIdentity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);

            // Guardamos físicamente la cookie en el navegador del usuario
            await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, new ClaimsPrincipal(claimsIdentity));

            // ==========================================
            // 🔄 REDIRECCIÓN EN BASE AL ROL DEL USUARIO
            // ==========================================
            switch (usuario_encontrado.Roles.Nombre)
            {
                case "Admin":
                    // El Administrador ingresa directo al Menú General de Inventario
                    return RedirectToAction("Menu", "Inventario");

                case "User":
                    // El rol "User" (Empleado) también entra al inventario, pero las restricciones se validan en las acciones
                    return RedirectToAction("Menu", "Inventario");

                case "Person":
                    return RedirectToAction("Registro", "Login");

                default:
                    return RedirectToAction("Menu", "Inventario");
            }
        }

        // Método extra muy útil para cuando deseen cerrar sesión de forma segura
        [HttpGet]
        public async Task<IActionResult> Salir()
        {
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            return RedirectToAction("Login", "Login");
        }
    }
}
namespace ProductosBreeze1.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {

        }
        public DbSet<Usuario> Usuarios { get; set; }
        public DbSet<Roles> Roles { get; set; }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Usuario>()
                .HasOne(u => u.Roles)
                .WithMany(r => r.Usuarios)
                .HasForeignKey(u => u.RolId);

            modelBuilder.Entity<Roles>().HasData(
                new Roles { IdRol = 1, Nombre = "Admin" },
                new Roles { IdRol = 2, Nombre = "User" },
                new Roles { IdRol = 3, Nombre = "Person" }
            );

            modelBuilder.Entity<Usuario>().HasData(
                new Usuario { idUsuario = 1, NameUser = "Juan Perez", Email = "juanito@gmail.com", Password = "123456", RolId = 2 }
            );
            base.OnModelCreating(modelBuilder);

        }

        public DbSet<Producto> Productos { get; set; }
            public DbSet<HistorialIngreso> HistorialIngresos { get; set; }
            public DbSet<Venta> Ventas { get; set; }
            public DbSet<DetalleVenta> DetallesVentas { get; set; }
    }
}
namespace ProductosBreeze1.Models
{
    public class DetalleVenta
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int VentaId { get; set; }
        public virtual Venta Venta { get; set; }

        [Required]
        public int ProductoId { get; set; }
        public virtual Producto Producto { get; set; }

        [Required]
        public int Cantidad { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal PrecioUnitario { get; set; }
    }
}
namespace ProductosBreeze1.Models
{
    public class ErrorViewModel
    {
        public string? RequestId { get; set; }

        public bool ShowRequestId => !string.IsNullOrEmpty(RequestId);
    }
}
namespace ProductosBreeze1.Models
{
    public class HistorialIngreso
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string Empleado { get; set; }

        [Required]
        public int ProductoId { get; set; }
        public virtual Producto Producto { get; set; }

        [Required]
        [Range(1, int.MaxValue, ErrorMessage = "La cantidad debe ser mayor a 0.")]
        public int Cantidad { get; set; }

        [Required]
        public DateTime FechaHora { get; set; }
    }
}
namespace ProductosBreeze1.Models
{
    public class Producto
    {
        [Key]
        public int Id { get; set; }

        [Required(ErrorMessage = "El nombre del producto es obligatorio.")]
        [StringLength(100)]
        public string Nombre { get; set; }

        [Required(ErrorMessage = "La marca es obligatoria.")]
        [StringLength(50)]
        public string Marca { get; set; }

        [Required(ErrorMessage = "La categoría es obligatoria.")]
        [StringLength(50)]
        public string Categoria { get; set; }
        public string UnidadMedida { get; set; } = string.Empty;

        [Column(TypeName = "decimal(18,2)")]
        public decimal CantidadMedida { get; set; }

        [Required(ErrorMessage = "El precio es obligatorio.")]
        [Column(TypeName = "decimal(18,2)")]
        [Range(0.01, double.MaxValue, ErrorMessage = "El precio debe ser mayor a 0.")]
        public decimal Precio { get; set; }

        [Required(ErrorMessage = "El stock inicial es obligatorio.")]
        [Range(0, int.MaxValue, ErrorMessage = "El stock no puede ser negativo.")]
        public int Stock { get; set; }
    }
}
namespace ProductosBreeze1.Models
{
    public class Roles
    {
        [Key, DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int IdRol { get; set; }
        [Required, StringLength(50)]
        public string Nombre { get; set; }
        public ICollection<Usuario> Usuarios { get; set; }
    }
}
namespace ProductosBreeze1.Models
{
    public class Usuario
    {
        [Key, DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int idUsuario { get; set; }
        [Required, StringLength(50)]
        public string NameUser { get; set; }
        [Required, StringLength(50)]
        public string Email { get; set; }
        [Required, StringLength(50)]
        public string Password { get; set; }
        public int RolId { get; set; }
        public Roles Roles { get; set; }
    }
}
namespace ProductosBreeze1.Models
{
    public class Venta
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string Empleado { get; set; }

        [Required(ErrorMessage = "El nombre del cliente es obligatorio.")]
        public string Cliente { get; set; }

        [Required]
        public DateTime FechaHora { get; set; }

        [Required]
        public string MetodoPago { get; set; } // Efectivo, Yape, Transferencia

        [Column(TypeName = "decimal(18,2)")]
        public decimal Total { get; set; }

        public virtual List<DetalleVenta> Detalles { get; set; } = new List<DetalleVenta>();
    }
}
namespace ProductosBreeze1.ViewModels
{
    public class LoginVM
    {
        public string Email { get; set; }
        public string Password { get; set; }
    }
}
namespace ProductosBreeze1.ViewModels
{
    public class UserVM
    {
        public string Name { get; set; }
        public string Email { get; set; }
        public string Pass { get; set; }
        public string RepPass { get; set; }
        public int IdRol { get; set; }
    }
}
