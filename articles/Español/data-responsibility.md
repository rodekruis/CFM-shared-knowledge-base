# [TEST] Marco de Responsabilidad de Datos
 
### Propósito
 
Este documento proporciona una visión general clara de las responsabilidades sobre los datos para las Sociedades Nacionales (SN) que participan en la Plataforma de Gestión de Retroalimentación. Define quién es responsable de los datos, cómo se procesan y qué obligaciones conlleva cada rol.
 
### Resumen de la Plataforma
 
- **Plataforma:** Plataforma de Gestión de Retroalimentación (EspoCRM) y KoboToolbox.
- **Operado por:** Cruz Roja Neerlandesa (NLRC).
- **SN incluidas:** Cualquier Sociedad Nacional incorporada formalmente a la Plataforma de Gestión de Retroalimentación.
- **Propósito:** Recopilar, gestionar y dar seguimiento a la retroalimentación de la comunidad enviada a la SN mediante formularios digitales (KoboToolbox) o entrada directa (EspoCRM).
- **Segregación de datos:** A cada SN se le asigna un equipo dentro de la Plataforma de Gestión de Retroalimentación, lo que garantiza que el personal solo pueda acceder a la retroalimentación relacionada con su propia SN.
- **Indicador de sensibilidad:** La retroalimentación puede marcarse como sensible, restringiendo el acceso únicamente a los roles autorizados.

### Roles y Responsabilidades de los Datos
 
| Role | Who | Key Responsibilities | Access in EspoCRM |
|------|-----|----------------------|-------------------|
| **Responsable del Tratamiento** | SN participante | • Determina el propósito y los medios del procesamiento<br>• Garantiza la base legal para la recopilación de datos<br>• Responsable de los derechos de los titulares de los datos<br>• Inicia y firma un Acuerdo de Intercambio de Datos con NLRC | Varía según el rol de usuario asignado |
| **Encargado del Tratamiento** | Cruz Roja Neerlandesa (NLRC) | • Aloja y opera la instancia de EspoCRM [Azure West Europe – Amsterdam]<br>• Procesa datos solo siguiendo instrucciones de la SN<br>• Implementa medidas de seguridad técnicas y organizativas<br>• Apoya a la SN en la DPIA si es necesario<br>• Notifica a la SN sobre cualquier violación de datos | Administrador de EspoCRM: acceso a todo el sistema solo para configuración y mantenimiento |
| **Encargado del Tratamiento** | IFRC (aloja KoboToolbox) | • Aloja y opera la plataforma KoboToolbox (en AWS Frankfurt, Alemania) para el envío de formularios y la recopilación de datos<br>• Procesa datos de retroalimentación en nombre de la SN antes de su transmisión a EspoCRM<br>• Aplica medidas de seguridad a los datos en tránsito y en reposo<br>• Sujeto al marco de protección de datos de IFRC | Los datos se transmiten a EspoCRM mediante API al enviar el formulario |
| **Administrador de la Plataforma (KoboToolbox)** | Administrador de Kobo (NLRC) | • Gestiona la configuración de formularios de KoboToolbox<br>• Garantiza el etiquetado correcto del equipo (SN, indicador de sensibilidad) al enviar formularios | Administrador de Kobo: acceso a la gestión de formularios |
| **Usuario de API** | Cuenta técnica gestionada por NLRC | • Facilita la transmisión automatizada entre KoboToolbox y EspoCRM<br>• Gestionada y supervisada por el Encargado del Tratamiento de NLRC | • Acceso a nivel de sistema limitado al equipo de SN asignado<br>• Usuario solo para fines de integración |
| **Gestor de Retroalimentación** | Personal de la SN (supervisión) | • Supervisa la gestión de la retroalimentación dentro de la SN<br>• Asigna el seguimiento a puntos focales<br>• Garantiza respuestas oportunas y adecuadas | • Crear, leer, editar y archivar toda la retroalimentación de la SN<br>• Asignar puntos focales<br>• Recibir notificaciones por correo electrónico |
| **Editor/Creador de Retroalimentación** | Personal de la SN (operativo) | • Introduce retroalimentación directamente en EspoCRM<br>• Da seguimiento a la retroalimentación asignada personalmente | • Crear retroalimentación<br>• Leer y editar solo la retroalimentación asignada a sí mismo |
| **Recopilador de Retroalimentación** | Personal o voluntario de la SN | • Envía retroalimentación de la comunidad en nombre de personas mediante KoboToolbox desde un enlace con código QR o la aplicación móvil KoboCollect<br>• No accede a EspoCRM | • Sin acceso<br>• Los datos ingresan a EspoCRM automáticamente al enviarse mediante KoboToolbox |
| **Gestor de Retroalimentación Sensible** | Personal de la SN (acceso restringido) | • Gestiona casos de retroalimentación sensible<br>• Debe cumplir estrictas obligaciones de confidencialidad | Leer y editar retroalimentación marcada como sensible |
| **Visualizador de Informes** | Personal de la SN / dirección | • Supervisa tendencias y el desempeño de los programas<br>• Usa los datos para mejorar los programas | • Leer informes (solo)<br>• Sin acceso a registros individuales |
| **Soporte al Cliente** | Personal de soporte de NLRC | • Proporciona soporte técnico a los usuarios de la SN<br>• No accede al contenido de la retroalimentación en operaciones normales | Acceso limitado: solo para fines de soporte |

### Datos Procesados
 
- **Naturaleza:** Retroalimentación de la comunidad enviada por o en nombre de personas.
- **Puede incluir Información de Identificación Personal (PII):** Nombres, datos de contacto, ubicación y descripciones de experiencias o quejas individuales.
- **Datos sensibles:** La retroalimentación puede marcarse como sensible. El acceso está restringido al rol de Gestor de Retroalimentación Sensible.
- **Flujo de datos:**
  - KoboToolbox (envío de formularios) a EspoCRM (almacenamiento, seguimiento, informes)
  - Entrada directa por parte del personal de la SN en EspoCRM
  - La segregación basada en equipos garantiza que cada SN solo acceda a sus propios datos
- **Transferencias internacionales:** Los datos se procesan dentro de EspoCRM alojado por NLRC. Las SN fuera del Espacio Económico Europeo (EEE) deben tener en cuenta que deben confirmarse las salvaguardias de transferencia aplicables.

### Gobernanza y Base Legal
 
- **Base legítima:** La Plataforma de Gestión de Retroalimentación apoya a las Sociedades Nacionales en la recopilación y respuesta a la retroalimentación de la comunidad como parte de sus programas humanitarios. Cada SN participante, como Responsable del Tratamiento, es responsable de confirmar la base legal adecuada conforme a las normas nacionales aplicables y a los estándares de protección de datos de la Cruz Roja y de la Media Luna Roja.
- **Acuerdo de Intercambio de Datos (DSA):** Se requiere un DSA entre cada SN participante (como Responsable del Tratamiento) y NLRC (como Encargado del Tratamiento) antes de la incorporación. Este acuerdo debe cubrir: alcance y propósito del procesamiento, obligaciones de seguridad, notificación de violaciones, acuerdos con subencargados y apoyo a los derechos de los titulares de los datos.
- **Período de conservación:** Los datos personales recopilados a través de la plataforma se conservarán durante un máximo de 2 años desde la recopilación de datos, tras lo cual se eliminarán o anonimizarán. Los datos no podrán almacenarse durante más tiempo del necesario para el propósito para el que fueron recopilados.
- **Evaluación de Impacto relativa a la Protección de Datos (DPIA):** Dado que se recopila PII, las SN participantes deben evaluar la necesidad de una DPIA, en particular cuando se procese retroalimentación sensible o la SN atienda a poblaciones vulnerables. NLRC brindará apoyo con información técnica pertinente. [El requisito de DPIA debe evaluarse por cada SN].
- **Normas aplicables:** NLRC se adhiere a los principios del Reglamento General de Protección de Datos (GDPR). Se espera que las SN cumplan con su propia legislación nacional de protección de datos y con las políticas aplicables de protección de datos de la Cruz Roja y de la Media Luna Roja.

### Contacto
 
- **Contacto del Encargado del Tratamiento de la Cruz Roja Neerlandesa:** Daan Gorsse (dgorsse@redcross.nl)
- **Violación de datos o inquietudes:** Notifique a NLRC de inmediato. El Responsable del Tratamiento de la SN es responsable de notificar a la autoridad supervisora pertinente dentro del plazo aplicable.
---

*Al completar el Acuerdo de Intercambio de Datos con la Sociedad Nacional, utilice la plantilla adjunta. Algunas notas adicionales relacionadas con las siguientes secciones de la plantilla:*
 
- *Fundamentos legales para compartir datos personales (elija la base legal más adecuada de las que se enumeran a continuación y explique claramente por qué es una base legal adecuada)*
- *Alcance (Marque lo que corresponda)*
- *Licencias (complételo solo si corresponde)*
*Como referencia:* [Plantilla de Acuerdo de Procesamiento de Datos GDPR](https://gdpr.eu/data-processing-agreement/)