# [TEST] Roles y permisos

### Propósito

Documentar los roles y permisos de los usuarios es esencial para garantizar claridad, seguridad y responsabilidad dentro de la Plataforma de Gestión de Retroalimentación. Ayudará a comprender quién puede acceder, modificar o gestionar secciones específicas de la plataforma y sus datos. Esto reducirá el riesgo de configuraciones incorrectas, accesos no autorizados y errores operativos. También respalda la incorporación, la auditoría y el cumplimiento al proporcionar una referencia confiable sobre el comportamiento del sistema. 

Puede encontrarse una visión general más detallada de la gestión de roles en la [documentación oficial de EspoCRM](https://docs.espocrm.com/administration/roles-management/). 

### Acceso a la Plataforma de Gestión de Retroalimentación

Las Sociedades Nacionales tienen la capacidad de acceder a la Plataforma de Gestión de Retroalimentación. Dado que esta es una plataforma compartida, a cada Sociedad Nacional se le asigna un Equipo, lo que le permite acceder **SOLO** a sus datos y visualizaciones de retroalimentación.

Dentro de la estructura de Equipo por Sociedad Nacional, varios usuarios de la Sociedad Nacional pueden vincularse al Equipo correspondiente para obtener acceso. Dependiendo de los roles y permisos específicos del usuario, este puede crear, leer, editar y/o eliminar datos de retroalimentación.

---

### Roles de la Sociedad Nacional

#### Supervisor de Retroalimentación

Este rol está designado para el punto focal de CEA de la SN en la sede central. Esta persona supervisará, monitoreará y gestionará la retroalimentación recibida y proporcionada a la comunidad. Es la principal persona de contacto para la SN en caso de cualquier problema con la plataforma.

Lo que puede hacer en la plataforma:

- Leer, crear, editar y eliminar registros de retroalimentación
  - Ejemplo: eliminar registros de retroalimentación después de incorporar al personal y a los voluntarios, para quitar entradas de prueba de la plataforma
  - Nota: aparte de las entradas de prueba, no es una buena práctica eliminar datos de retroalimentación
- Crear o eliminar usuarios mediante la entidad "User Access Requests"
- Asignar usuarios para dar seguimiento a registros específicos de retroalimentación
- Dar seguimiento en el stream con otros colegas
- Leer informes
- Autorizado para registros de retroalimentación sensibles
  - Puede leer, editar, asignar usuarios y dar seguimiento a retroalimentación sensible

#### Punto Focal de Retroalimentación

Este rol está designado para miembros de la SN (p. ej., CEA, PMER, IM, sucursales, operadores de línea directa) que gestionarán la retroalimentación ingresada en la Plataforma de Gestión de Retroalimentación. 

Lo que puede hacer en la plataforma:

- Leer, crear y editar registros de retroalimentación
- Asignar usuarios para dar seguimiento a registros específicos de retroalimentación (si se conocen los usuarios)
- Dar seguimiento a registros de retroalimentación
- Dar seguimiento en el stream con otros colegas
- Leer informes


#### Gestor de Retroalimentación

Este rol está designado para miembros de la SN (p. ej., puntos focales de CVA, Salud, Refugio) que gestionarán o simplemente verán retroalimentación específica.

Lo que puede hacer en la plataforma:

- Leer y editar los registros de retroalimentación asignados a ellos
- Dar seguimiento a los registros de retroalimentación asignados a ellos
- Dar seguimiento en el stream con otros colegas
- Leer informes


#### Punto Focal de Retroalimentación Sensible

Este rol está designado para el punto focal de la SN (p. ej., punto focal de PGI) que gestionará retroalimentación sensible. Cuando un registro de retroalimentación se marca como sensible, SOLO los usuarios con este rol y los Supervisores de Retroalimentación podrán acceder, ver y editar el registro de retroalimentación.

Lo que puede hacer en la plataforma:

- Leer y editar registros de retroalimentación sensibles
- Dar seguimiento y cerrar registros de retroalimentación sensibles
- Leer informes


#### Visualizador de Informes de Retroalimentación

Este rol está designado para usuarios de la SN que necesitan una visión general de alto nivel de la retroalimentación. El Visualizador de Informes de Retroalimentación, por ejemplo, podría ser alguien del equipo de PMER que necesita datos para informes o podría ser el Secretario General que quisiera tener una visión general del trabajo. NO pueden ver ninguna Información de Identificación Personal en el registro de retroalimentación.

Lo que puede hacer en la plataforma:

- Acceso al panel para informes
- Acceso de alto nivel a registros de retroalimentación sin PII

---

### Roles de Soporte
 
#### Soporte al Cliente
 
Este rol está designado para el Equipo de Datos 510 de la Cruz Roja Neerlandesa. El equipo de Soporte al Cliente abordará y solucionará cualquier problema que enfrente la SN al utilizar la Plataforma Regional de Gestión de Retroalimentación.
 
Lo que se puede esperar de ellos:
 
- Soporte de nivel 1 y 2
  - Nivel 1: invitar usuarios, restablecer contraseñas, ayudar a los usuarios a navegar por la Interfaz de Usuario (UI), explicar cómo EspoCRM está (o no está) pensado para usarse, actualizar un campo
- Solución de errores
- Soporte a usuarios

#### Administrador
 
Este rol está designado para el Equipo de Datos 510 de la Cruz Roja Neerlandesa.
 
Lo que se puede esperar de ellos:
 
- Soporte de nivel 1, 2 y 3
  - Nivel 1: invitar usuarios, restablecer contraseñas, ayudar a los usuarios a navegar por la Interfaz de Usuario (UI), explicar cómo EspoCRM está (o no está) pensado para usarse, actualizar un campo
  - Nivel 2: agregar un nuevo campo, crear una nueva entidad, relacionar 2 entidades entre sí, automatizar una tarea (diagramas de flujo)
  - Nivel 3: configurar el servidor en el que se aloja EspoCRM, instalar/actualizar EspoCRM, crear/restaurar una copia de seguridad, actualizar la configuración de red.
- Actualizaciones y configuraciones de la plataforma
- Agregar Equipos de Sociedades Nacionales e incorporarlos a la plataforma
- Desarrollar informes y mantener el panel de la página de inicio
- Mantener diagramas de flujo e integraciones de API

#### Recolector de Datos de Retroalimentación (Ver Formulario Kobo)
 
Este rol no es un rol de EspoCRM, sino únicamente un rol en la cuenta de KoboToolbox del recolector de datos de retroalimentación de la SN que necesita acceso sin conexión al formulario de KoboToolbox. Este rol puede solicitarse a través del punto focal de la SN (Gerente de Retroalimentación), que tiene acceso al formulario.