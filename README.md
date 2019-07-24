# miniapp
Prueba técnica de Backend

<h3>Cronograma de actividades y seguimiento</h3>
<table>
  <tr>
    <td>Item</td>
    <td>Obligatorio</td>
    <td>Actividad</td>
    <td>Duración proyectada (Horas)</td>
    <td>Duración consumida (Horas)</td>
    <td>Estado </td>
  </tr>
   <tr>
    <td>1</td>
    <td>Si</td>
    <td>Analisis de requisitos funcionales y no funcionales</td>
    <td>1</td>
    <td>1</td>
    <td>Completada</td>
  </tr>
  <tr>
    <td>2</td>
    <td>Si</td>
    <td>Revisión de la documentacion del API de Tpaga</td>
    <td>1</td>
    <td>1</td>
    <td>Completada</td>
  </tr>
  <tr>
    <td>3</td>
    <td>Si</td>
    <td>Planificación del desarrollo, elección de herramientas y tecnólogias a utilizar</td>
    <td>1</td>
    <td>1</td>
    <td>Completada</td>
  </tr>
  <tr>
    <td>4</td>
    <td>Si</td>
    <td>Configuración del entorno de trabajo</td>
    <td>1</td>
    <td>1</td>
    <td>Completada</td>
  </tr>
  <tr>
    <td>5</td>
    <td>Si</td>
    <td>Definición de modelos de persistencia de datos y configuración del sitio de administración de la miniapp</td>
    <td>1</td>
    <td>2</td>
    <td>Completada</td>
  </tr>
    <tr>
    <td>6</td>
    <td>Si</td>
    <td>Desarrollar el servicio de autenticación a la miniapp</td>
    <td>1</td>
    <td>NA</td>
    <td>Por ejecutar</td>
  </tr>
  <tr>
    <td>7</td>
    <td>Si</td>
    <td>Desarrollar el servicio Restfull de compra con la billetera</td>
    <td>2</td>
    <td>3</td>
    <td>Completada</td>
  </tr>
  <tr>
    <td>8</td>
    <td>Si</td>
    <td>Desarrollar el servicio Restfull para verificar el pago</td>
    <td>3</td>
    <td>2</td>
    <td>Completado</td>
  </tr>
  <tr>
    <td>9</td>
    <td>Si</td>
    <td>Desarrollar el servicio Restfull para listar operaciones y el estado de las operaciones</td>
    <td>1</td>
    <td>1</td>
    <td>Completado</td>
  </tr>
  <tr>
    <td>10</td>
    <td>Si</td>
    <td>Maquetar el frontend de la miniapp.</td>
    <td>1</td>
    <td>2</td>
    <td>Completado</td>
  </tr> 
  <tr>
    <td>11</td>
    <td>Si</td>
    <td>Consumir el servicio Resfull de autenticacion a la miniapp.</td>
    <td>1</td>
    <td>NA</td>
    <td>Por ejecutar</td>
  </tr>

  <tr>
    <td>12</td>
    <td>Si</td>
    <td>Desarrollar frontend para registrar el producto y la cantidad a comprar, consumir el servicio Restfull de compra con la billetera y mostrar al usuario los resultados de la compra.</td>
    <td>3</td>
    <td>3</td>
    <td>Completado</td>
  </tr>
  <tr>
    <td>13</td>
    <td>Si</td>
    <td>Desarrollar frontend para listar consumir el servicio restfull de lista de operaciones y el estado de cada una.<b>El admin de Django provee una opcion para mostrar la lista de operaciones y el estado de cada una, el cual se actualiza al consultar el API de Tpaga con el estado que retorna este recurso.</b></td>
    <td>2</td>
    <td>NA</td>
    <td>Por ejecutar</td>
  </tr>
  <tr>
    <td>15</td>
    <td>No</td>
    <td>Desarrollar backend y frontend para reversar un pago.</td>
    <td>1</td>
    <td>NA</td>
    <td>Por ejecutar</td>
  </tr>
  <tr>
    <td>16</td>
    <td>No</td>
    <td>Despliegue de la miniapp (AWS).</td>
    <td>1</td>
    <td>1</td>
    <td>Completado</td>
  </tr>
    <tr>
    <td>17</td>
    <td>No</td>
    <td>Instrucciones para pruebas.</td>
    <td>1</td>
    <td>1</td>
    <td>Completado</td>
  </tr>
   <tr>
    <td>18</td>
    <td>No</td>
    <td>Recomendaciones.</td>
    <td>1</td>
    <td>1</td>
    <td>Completado</td>
  </tr>
  <tr>
    <td colspan="3">Total</td>
    <td> 23 </td>
    <td> 20 </td>
    <td> En ejecución </td>
  </tr>
</table>


<h3>Tecnólogias a utilizar</h3>
<ul>
  <li>Lenguaje de programación: Python</li>
  <li>Framework de desarrollo: Django</li>
  <li>Motor de base de datos: Postgree</li>
  <li>frontend: HTML + CSS3 + knockout</li>
  <li>Control de versiones: Github</li>
  <li>Despliegue: EC2 de AWS</li>
</ul>

<h3>Servicios Resfull</h3>
<ul>
  <li>
    </b>servicio para creacion de solicitud de pago:</b>
    http://localhost:8000/api/operation/create-payment-request/
    Se espera recibir por POST el parametro data que envia un array de json que contenga
    los id de los productos a comprar y su respectiva cantidad
    [{id:xx, quantity: yy}, {id:xx1, quantity: yy1}, ....]
    igualmente se espera el parametro user id del usuario que esta realizando la peticion
  </li>
  <li>
  </b>servicio para verificar el estado de la solicitud de pago:</b>
  http://localhost:8000/api/operation/get-status-payment-request
  se envia el parametro token que corresponde al token retornado por el 
  servicio de creacion de la solicitud de pago.
  </li>
  <li>
    </b>servicio para listar solicitudes de pago:</b>
    http://localhost:8000/api/operation/
     es posible realizar la consulta utilizando los parametros(pueden combinarse) 
     idempotency_token, token, status, user
  </li>
</ul>

<h3>Instrucciones de instalacion</h3>
<ul>
  <li>
    instalar Python con las librerias auxiliares: pip3, easy_install, entre otras.
  </li>
  <li>
    instalar virtualenv con el comando: easy_install virtualenv (alternativamente puede utilizar pip en lugar de easy_install)
  </li>
  <li>
    crear el ambiente virtual usando python 3.5.2 o superior a traves del comando: virtualenv [nombre del entorni virtual]
  </li>
  <li>
    activar el entorno virtual: ingrese a la carpeta del entorno virtual creado y utilice el comando: activate
  </li>
  <li>
    descargue el repositorio de github en la carpeta Scripts del entorno virtual creado
  </li>
  <li>
    instalar postgree y pgadmin si no lo tiene instalado.
  </li>
  <li>
    entrar al admin de postgree, usando pgadmin, y crear la base de datos vacia con el nombre miniappcomercio
  </li>
  <li>crear migraciones de los modelos a la base de datos creada usando el comando: python35 manage.py makemigrations</li>
  <li>migrar los modelos hacia la base de datos usando el comando: python35 manage.py migrate</li>
  <li>entrar al archivo settings.py ubicado en la ruta [ruta entorno virtual]\Scripts\miniapp\miniapp y buscar la constante IP_SERVER asignandole lo siguiente: https://[direccion ip del server]:8000/ luego guarde el cambio del archivo</li>
  <li>ejecutar el proyecto con el comando Python35 manage.py runserver</li>
  <li>entrar al admin de django y en el grupo products crear los productos que se venderan en el sitio del comercio</li>
</ul>

<h3>Observaciones</h3>
<p align="justify">
  la app de TPaga se detiene al utilizar el link q retorna el API de Tpaga en la propiedad tpaga_payment_url.
  pregunté en slack pero no hubo respuesta acerca de como solucionar el tema.
</p>

<p align="justify">
  el link a la documentacion de Miniapps esta errado en el documento
de la prueba, el link es https://payment-links.docs.tpaga.co/
</p>
<p align="justify">
  se sugiere utilizar repositorios privados, debido a que se 
debe escribir en el codigo el usuario y la contraseña para acceder
a la API de Tpaga, dejarlos en repositorios publicos expone las
credenciales de autenticacion. Si se realizan repositorios privados, 
es necesario especificar los usuarios con los cuales se debe compartirlo.
 </p>
 

