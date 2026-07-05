# [TEST] Retroalimentación Sensible
 
### 1. Propósito
 
Garantizar que la retroalimentación clasificada como sensible por la Sociedad Nacional (NS) se gestione de forma segura, coherente y únicamente por personas autorizadas designadas.
 
### 2. Definición
 
La retroalimentación sensible es una categoría de retroalimentación definida por la Sociedad Nacional (NS), que solo puede ser gestionada por personas responsables específicamente designadas.
 
La retroalimentación sensible puede clasificarse de diferentes maneras, pero aquí hay 2 distinciones principales que se deben tener en cuenta, ya que el seguimiento se realizará de manera diferente:
 
- Incumplimientos del código de conducta (ejemplo: corrupción/fraude/VBG cometidos por personal o voluntarios de la Cruz Roja)
- Retroalimentación que es sensible para la situación personal de alguien (ejemplo: salud, estigma, violencia doméstica).

### 3. Funciones y Responsabilidades
 
- **Recolector de Retroalimentación**
  - Registra la retroalimentación en Kobo.
  - Marca la retroalimentación como sensible cuando corresponda.
- **Gestor de Retroalimentación**
  - Revisa la retroalimentación entrante.
  - Confirma si la retroalimentación es sensible según las definiciones de la NS.
  - Asigna un Gestor de Retroalimentación Sensible designado.
  - Garantiza que se realice el seguimiento.
  - Configuraciones de cuenta de usuario: *[capturas de pantalla: ajustes de rol/permisos]*
- **Creador y Editor de Retroalimentación (Persona Autorizada – Gestor de Retroalimentación Sensible)**
  - Gestiona el caso de principio a fin.
  - Garantiza el seguimiento y la documentación adecuados.
  - Actualiza el estado y cierra el caso.
  - Configuraciones de cuenta de usuario: *[capturas de pantalla: ajustes de rol/permisos]*
- **Sistema (Kobo / EspoCRM)**
  - Establece automáticamente la prioridad en *Alta* cuando la retroalimentación se marca como sensible.
  - Autoriza automáticamente a los Gestores de Retroalimentación para gestionar retroalimentación sensible (según los roles/permisos definidos por la NS).
  - Verifica que cualquier persona asignada esté autorizada para gestionar retroalimentación sensible.
  - Establece el estado del caso en *En Progreso* al momento de la asignación.
  - Envía notificaciones y recordatorios.

### 4. Procedimiento
 
#### Paso 1: Recolección y Registro de la Retroalimentación
 
- La retroalimentación se recopila y se registra en Kobo.
- Si corresponde, el Recolector de Retroalimentación marca la retroalimentación como **sensible**.
- Si no se sabe si la retroalimentación es sensible, dejar en blanco.

#### Paso 2: Acciones Automáticas del Sistema
 
- El sistema automáticamente:
  - Establece la prioridad en **Alta**.
  - Dirige la retroalimentación para su revisión.

#### Paso 3: Revisión y Validación
 
- El Gestor de Retroalimentación:
  - Revisa la retroalimentación.
  - Confirma si cumple con la definición de retroalimentación sensible de la NS.
- Si **no es sensible**:
  - Desmarcar como sensible.
  - Restablecer la prioridad.
  - Procesar según los procedimientos estándar de retroalimentación.
- Si **es sensible**:
  - Continuar con el Paso 4.

#### Paso 4: Asignación
 
- El Gestor de Retroalimentación asigna el caso a un **Gestor de Retroalimentación Sensible** designado.
- El sistema establece el estado del caso en **En Progreso**.

#### Paso 5: Notificación y Monitoreo
 
- El Gestor de Retroalimentación Sensible asignado:
  - Recibe una notificación por correo electrónico y EspoCRM.
- El sistema:
  - Envía recordatorios diarios hasta que el caso sea actualizado.

#### Paso 6: Gestión del Caso
 
- El Gestor de Retroalimentación Sensible:
  - Revisa el caso.
  - Toma las medidas apropiadas.
  - Sigue los procedimientos operativos estándar internos para la gestión de casos sensibles.
  - Comparte la retroalimentación internamente **si** es necesario y está permitido.

#### Paso 7: Actualizaciones de Estado
 
- El Gestor de Retroalimentación Sensible actualiza el estado del caso a medida que avanza el trabajo.

#### Paso 8: Cierre
 
- Una vez que el caso se resuelve:
  - El Gestor de Retroalimentación Sensible marca el caso como **cerrado**.
  - El cierre se confirma en el sistema de resumen.

### 5. Principios Clave
 
- La Sociedad Nacional define qué constituye retroalimentación sensible.
- Solo las personas autorizadas pueden gestionar retroalimentación sensible.
- La retroalimentación sensible está oculta para todos los demás usuarios, excepto para los usuarios autorizados.
- Todos los casos de retroalimentación sensible se tratan como de **alta prioridad**.
- El seguimiento oportuno es obligatorio y se monitorea activamente.

### 6. Riesgos
 
El incumplimiento de este SOP puede resultar en:
 
- Retrasos en la gestión de retroalimentación de alto riesgo.
- Incumplimientos de la confidencialidad o de los protocolos de protección.

### 7. Visual del flujo de trabajo
 
![Flujo de trabajo de retroalimentación sensible](../../assets/sensitive-feedback-flow.png)
 
### 8. Validación
 
- El protocolo necesita revisión antes de finales de 2026 para asegurar que siga siendo efectivo.