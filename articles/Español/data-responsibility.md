# [TEST] Marco de Responsabilidad de Datos
 
### Propósito
 
Este documento proporciona una visión general clara de las responsabilidades sobre los datos para las Sociedades Nacionales (NS) que participan en la Plataforma Regional de Gestión de Retroalimentación. Define quién es responsable de los datos, cómo se procesan y qué obligaciones conlleva cada función.
 
### Descripción general de la plataforma
 
- **Platform:** Plataforma Regional de Gestión de Retroalimentación (EspoCRM) y KoboToolbox.
- **Operated by:** Cruz Roja Neerlandesa (NLRC).
- **NS in scope:** Cualquier Sociedad Nacional incorporada formalmente a la Plataforma Regional de Gestión de Retroalimentación.
- **Purpose:** Recopilar, gestionar y dar seguimiento a la retroalimentación comunitaria enviada a la NS mediante formularios digitales (KoboToolbox) o entrada directa (EspoCRM).
- **Data segregation:** A cada NS se le asigna un equipo dentro de la Plataforma Regional de Gestión de Retroalimentación, lo que garantiza que el personal solo pueda acceder a la retroalimentación relacionada con su propia NS.
- **Sensitive flag:** La retroalimentación puede marcarse como sensible, restringiendo el acceso únicamente a funciones autorizadas.

### Funciones y responsabilidades de los datos
 
| Role | Who | Key Responsibilities | Access in EspoCRM |
|------|-----|----------------------|-------------------|
| **Data Controller** | NS participante | • Determina la finalidad y los medios del tratamiento<br>• Garantiza la base legal para la recopilación de datos<br>• Responsable de los derechos de los titulares de los datos<br>• Inicia y firma un Acuerdo de Intercambio de Datos con NLRC | Varía según la función de usuario asignada |
| **Data Processor** | Cruz Roja Neerlandesa (NLRC) | • Aloja y opera la instancia de EspoCRM [Azure West Europe – Amsterdam]<br>• Procesa datos solo siguiendo instrucciones de la NS<br>• Implementa medidas de seguridad técnicas y organizativas<br>• Apoya a la NS en la DPIA si es necesario<br>• Notifica a la NS sobre cualquier violación de datos | Administrador de EspoCRM: acceso a todo el sistema solo para configuración y mantenimiento |
| **Data Processor** | IFRC (aloja KoboToolbox) | • Aloja y opera la plataforma KoboToolbox (en AWS Frankfurt, Alemania) para el envío de formularios y la recopilación de datos<br>• Procesa datos de retroalimentación en nombre de la NS antes de su transmisión a EspoCRM<br>• Aplica medidas de seguridad a los datos en tránsito y en reposo<br>• Sujeto al marco de protección de datos de IFRC | Los datos se transmiten a EspoCRM mediante API al enviar el formulario |
| **Platform Admin (KoboToolbox)** | Administrador de Kobo (NLRC) | • Gestiona la configuración de formularios de KoboToolbox<br>• Garantiza el etiquetado correcto del equipo (NS, marca de sensible) al enviar formularios | Administrador de Kobo: acceso a la gestión de formularios |
| **API User** | Cuenta técnica gestionada por NLRC | • Facilita la transmisión automatizada entre KoboToolbox y EspoCRM<br>• Gestionada y supervisada por el Procesador de Datos de NLRC | • Acceso a nivel de sistema limitado al equipo NS asignado<br>• Usuario solo para fines de integración |
| **Feedback Manager** | Personal de la NS (supervisión) | • Supervisa la gestión de la retroalimentación dentro de la NS<br>• Asigna el seguimiento a puntos focales<br>• Garantiza respuestas oportunas y adecuadas | • Crear, leer, editar y archivar toda la retroalimentación de la NS<br>• Asignar puntos focales<br>• Recibir notificaciones por correo electrónico |
| **Feedback Editor/Creator** | Personal de la NS (operativo) | • Introduce retroalimentación directamente en EspoCRM<br>• Da seguimiento a la retroalimentación asignada personalmente | • Crear retroalimentación<br>• Leer y editar solo la retroalimentación propia asignada |
| **Feedback Collector** | Personal o voluntariado de la NS | • Envía retroalimentación comunitaria en nombre de personas mediante KoboToolbox desde un enlace con código QR o la aplicación móvil KoboCollect<br>• No accede a EspoCRM | • Sin acceso<br>• Los datos ingresan automáticamente en EspoCRM al enviarse mediante KoboToolbox |
| **Sensitive Feedback Manager** | Personal de la NS (acceso restringido) | • Gestiona casos de retroalimentación sensible<br>• Debe cumplir estrictas obligaciones de confidencialidad | Leer y editar retroalimentación marcada como sensible |
| **Report Viewer** | Personal de la NS / dirección | • Supervisa tendencias y desempeño del programa<br>• Usa los datos para mejorar el programa | • Leer informes (solo)<br>• Sin acceso a registros individuales |
| **Client Support** | Personal de soporte de NLRC | • Proporciona soporte técnico a usuarios de la NS<br>• No accede al contenido de la retroalimentación en operaciones normales | Acceso limitado: solo para fines de soporte |
 
### Datos procesados
 
- **Nature:** Retroalimentación comunitaria enviada por o en nombre de personas.
- **May include Personally Identifiable Information (PII):** Nombres, datos de contacto, ubicación y descripciones de experiencias o quejas individuales.
- **Sensitive data:** La retroalimentación puede marcarse como sensible. El acceso está restringido a la función de Gestor de Retroalimentación Sensible.
- **Data flow:**
  - KoboToolbox (envío de formularios) a EspoCRM (almacenamiento, seguimiento, informes)
  - Entrada directa por parte del personal de la NS en EspoCRM
  - La segregación por equipos garantiza que cada NS solo acceda a sus propios datos
- **International transfers:** Los datos se procesan dentro de EspoCRM alojado por NLRC. Las NS fuera del Espacio Económico Europeo (EEE) deben tener en cuenta que deben confirmarse las salvaguardias de transferencia aplicables.

### Gobernanza y base legal
 
- **Legitimate basis:** La Plataforma Regional de Gestión de Retroalimentación apoya a las Sociedades Nacionales en la recopilación y respuesta a la retroalimentación comunitaria como parte de sus programas humanitarios. Cada NS participante, como Responsable del Tratamiento, es responsable de confirmar la base legal adecuada conforme a las normas nacionales aplicables y a los estándares de protección de datos de la Cruz Roja y de la Media Luna Roja.
- **Data Sharing Agreement (DSA):** Se requiere un DSA entre cada NS participante (como Responsable del Tratamiento) y NLRC (como Encargado del Tratamiento) antes de la incorporación. Este acuerdo debe cubrir: alcance y finalidad del tratamiento, obligaciones de seguridad, notificación de violaciones de datos, acuerdos con subencargados y apoyo a los derechos de los titulares de los datos.
- **Retention period:** Los datos personales recopilados a través de la plataforma se conservarán durante un máximo de 2 años desde la recopilación de los datos, tras lo cual se eliminarán o anonimizarán. Los datos no podrán almacenarse durante más tiempo del necesario para la finalidad para la que fueron recopilados.
- **Data Protection Impact Assessment (DPIA):** Dado que se recopila PII, las NS participantes deben evaluar la necesidad de una DPIA, en particular cuando se procese retroalimentación sensible o la NS atienda a poblaciones vulnerables. NLRC brindará apoyo con información técnica pertinente. [DPIA requirement to be assessed per NS].
- **Applicable standards:** NLRC se adhiere a los principios del Reglamento General de Protección de Datos (GDPR). Se espera que las NS cumplan con su propia legislación nacional de protección de datos y con las políticas aplicables de protección de datos de la Cruz Roja y de la Media Luna Roja.

### Contacto
 
- **Data Processor contact from the Netherlands Red Cross:** Daan Gorsse (dgorsse@redcross.nl)
- **Data breach or concerns:** Notifique a NLRC de inmediato. El Responsable del Tratamiento de la NS es responsable de notificar a la autoridad supervisora pertinente dentro del plazo aplicable.
---

*Al completar el Acuerdo de Intercambio de Datos con la Sociedad Nacional, utilice la plantilla adjunta. Algunas notas adicionales relacionadas con las siguientes secciones de la plantilla:*
 
- *Fundamentos jurídicos para compartir datos personales (elija la base legal más adecuada de las que se enumeran a continuación y explique claramente por qué es una base legal adecuada)*
- *Alcance (marque lo que corresponda)*
- *Licencias (complételo solo si corresponde)*
*Como referencia:* [GDPR Data Processing Agreement Template](https://gdpr.eu/data-processing-agreement/)