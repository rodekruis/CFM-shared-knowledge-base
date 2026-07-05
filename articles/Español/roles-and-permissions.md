# [TEST] Roles y permisos

### Propósito

Documentar los roles y permisos de los usuarios es esencial para garantizar claridad, seguridad y responsabilidad dentro de la Plataforma de Gestión de Retroalimentación. Ayudará a comprender quién puede acceder, modificar o gestionar secciones específicas de la plataforma y sus datos. Esto reducirá el riesgo de configuraciones incorrectas, accesos no autorizados y errores operativos. También respalda la incorporación, la auditoría y el cumplimiento al proporcionar una referencia confiable sobre el comportamiento del sistema. 

Puede encontrarse una visión general más detallada de la gestión de roles en la [documentación oficial de EspoCRM](https://docs.espocrm.com/administration/roles-management/). 

### Acceso a la Plataforma de Gestión de Retroalimentación

Las Sociedades Nacionales tienen la capacidad de acceder a la Plataforma de Gestión de Retroalimentación. Dado que esta es una plataforma compartida, a cada Sociedad Nacional se le asigna un Equipo, lo que le permite acceder **SOLO** a sus datos y visualizaciones de retroalimentación.

Dentro de la estructura de Equipo por Sociedad Nacional, varios usuarios de la Sociedad Nacional pueden vincularse al Equipo correspondiente para obtener acceso. Dependiendo de los roles y permisos específicos del usuario, este puede crear, leer, editar y/o eliminar datos de retroalimentación.

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