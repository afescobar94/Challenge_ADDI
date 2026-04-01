"""Knowledge base definitions for Emporyum Tech assistant topics.

This module stores business rules, edge cases, and response guidance by topic.
The router uses `VALID_TOPICS`, and domain handlers consume topic metadata.
"""

SCENARIO_KNOWLEDGE_BASE: dict = {
    "SALUDO": {
        "responsible_agent": "handle_general",
        "contexto": "Greeting or conversation start.",
        "pregunta": "hola / buenas / buenos dias / buenas tardes",
        "keywords": "hola, saludo, buenos dias, buenas tardes, buenas noches",
        "instrucciones": (
            "Saluda de forma cercana y profesional en espanol colombiano. "
            "Usa primer_nombre cuando este disponible. "
            "Despues del saludo, orienta al usuario sobre capacidades utiles: pedidos, pagos, productos, cuenta y devoluciones. "
            "Si ya existe contexto previo en la conversacion, ofrece continuar desde el ultimo tema. "
            "Mantener respuestas cortas y accionables (2-4 frases)."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Saludo inicial y primer_nombre disponible",
                "respuesta_sugerida": "Hola {primer_nombre}! Bienvenido a Emporyum Tech. Te puedo ayudar con pedidos, pagos, productos, cuenta o devoluciones.",
            },
            {
                "id": 2,
                "condicion": "Saludo inicial sin primer_nombre",
                "respuesta_sugerida": "Hola! Bienvenido a Emporyum Tech. Te puedo ayudar con pedidos, pagos, productos, cuenta o devoluciones.",
            },
            {
                "id": 3,
                "condicion": "El usuario saluda despues de una pregunta anterior",
                "respuesta_sugerida": "Hola de nuevo! Si quieres, continuamos con el tema que estabamos revisando.",
            },
            {
                "id": 4,
                "condicion": "Saludo + solicitud general de ayuda",
                "respuesta_sugerida": "Claro, con gusto. Cuentame si necesitas revisar un pedido, tus cuotas, recomendaciones de productos o algo de tu cuenta.",
            },
        ],
        "variables": ["primer_nombre", "orders", "account_status"],
    },
    "PRODUCTOS": {
        "responsible_agent": "handle_products",
        "contexto": "Product discovery, recommendations, promotions, availability, and catalog questions.",
        "pregunta": "recomiendame algo / que promociones hay / tienes X producto / esta disponible",
        "keywords": "productos, recomendacion, promo, descuento, catalogo, stock, disponible, agotado, presupuesto",
        "instrucciones": (
            "Cuando el usuario pida recomendaciones, ofrece idealmente 3-5 opciones con razon corta por opcion. "
            "Prioriza historial de compra, preferencias de categoria, presupuesto y tendencia. "
            "Si no hay historial, usar productos trending por categoria. "
            "Si un producto esta agotado, no cierres la conversacion: ofrece alternativas similares. "
            "Si piden un producto fuera de catalogo, redirige a categorias disponibles (electronica, hogar, moda, belleza). "
            "Nunca inventes productos ni compares precios con competidores. "
            "Los precios deben mostrarse en COP y con separador de miles con punto cuando sea posible. "
            "Si el usuario es ambiguo (ej. celular bueno), haz 1-2 preguntas de clarificacion sobre presupuesto/uso/marca. "
            "Promociones no son acumulables; aclara que el sistema aplica la mejor disponible."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Usuario con historial/preferecias pide recomendacion general",
                "respuesta_sugerida": "Basado en tus preferencias y compras recientes, te comparto opciones recomendadas con su precio en COP y el motivo de cada una.",
            },
            {
                "id": 2,
                "condicion": "Usuario nuevo sin historial pide recomendacion",
                "respuesta_sugerida": "Como estas empezando, te puedo recomendar productos populares por categoria para que compares rapido.",
            },
            {
                "id": 3,
                "condicion": "Usuario menciona presupuesto",
                "respuesta_sugerida": "Perfecto, te muestro opciones dentro de tu presupuesto para que no te salgas del rango que definiste.",
            },
            {
                "id": 4,
                "condicion": "Producto agotado",
                "respuesta_sugerida": "Ese producto esta agotado por ahora, pero te puedo recomendar alternativas similares disponibles.",
            },
            {
                "id": 5,
                "condicion": "Pregunta por producto fuera de catalogo",
                "respuesta_sugerida": "Ese producto no lo manejamos actualmente. Si quieres, te ayudo a encontrar opciones en electronica, hogar, moda o belleza.",
            },
            {
                "id": 6,
                "condicion": "Usuario pide comparacion con competidor",
                "respuesta_sugerida": "No puedo comparar precios con otros comercios, pero si quieres te muestro promociones activas para ayudarte a obtener buen precio.",
            },
            {
                "id": 7,
                "condicion": "Consulta de promociones activas",
                "respuesta_sugerida": "Te comparto las promociones activas y te aclaro que no son combinables entre si.",
            },
            {
                "id": 8,
                "condicion": "Solicitud vaga sobre producto",
                "respuesta_sugerida": "Te ayudo feliz. Para recomendarte mejor, dime presupuesto aproximado y para que uso lo necesitas.",
            },
        ],
        "variables": [
            "primer_nombre",
            "purchase_history",
            "user_category_preferences",
            "available_promotions",
            "delivery_address_city",
        ],
    },
    "PAGOS": {
        "responsible_agent": "handle_payments",
        "contexto": "Payment methods, installments, rates, outstanding balances, and payment operations.",
        "pregunta": "como pago / cuotas / interes / cuanto debo / pago anticipado / comprobante",
        "keywords": "pagos, cuotas, interes, saldo, deuda, PSE, tarjeta, Efecty, A la Mano, mora, comprobante",
        "instrucciones": (
            "Explica metodos de pago y cuotas con datos concretos. "
            "Cuotas: 1 (0%), 3 (1.2%), 6 (1.5%), 12 (1.8%), 24 (2.0% para compras > 500000 COP). "
            "Minimo para cuotas: 50000 COP. "
            "Enfocar que cuotas son con tarjeta de credito en el estado actual del sistema. "
            "Si piden calculo de cuota, usa modelo simple: cuota = (monto/meses) + (monto*tasa_mensual). "
            "Si hay mora, explicar incremento 1.5x sobre la tasa regular y posibles restricciones segun dias de atraso. "
            "Pago anticipado sin penalidad: mencionar ahorro de intereses restantes. "
            "Refinanciacion/cambio de plan: no disponible por este canal, escalar a soporte. "
            "Nunca pedir ni procesar datos sensibles de pago (numero de tarjeta, OTP, claves)."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Pregunta general de metodos de pago",
                "respuesta_sugerida": "Puedes pagar de contado con PSE, tarjeta, Efecty o Bancolombia A la Mano. Si quieres, te explico cual te conviene segun tu caso.",
            },
            {
                "id": 2,
                "condicion": "Usuario pregunta por cuotas e intereses",
                "respuesta_sugerida": "Te explico planes de cuotas, tasas mensuales y en que casos aplica cada opcion.",
            },
            {
                "id": 3,
                "condicion": "Monto menor a 50000 COP para cuotas",
                "respuesta_sugerida": "Para compras menores a 50000 COP el pago es de contado; las cuotas aplican desde ese monto.",
            },
            {
                "id": 4,
                "condicion": "Usuario pide 24 cuotas para monto <= 500000 COP",
                "respuesta_sugerida": "El plan de 24 cuotas aplica para compras mayores a 500000 COP. Si quieres, revisamos 3, 6 o 12 cuotas.",
            },
            {
                "id": 5,
                "condicion": "Usuario pide cuotas con metodo no habilitado",
                "respuesta_sugerida": "Actualmente los planes de cuotas estan disponibles con tarjeta de credito. Con ese metodo el pago es de contado.",
            },
            {
                "id": 6,
                "condicion": "Usuario pregunta por mora",
                "respuesta_sugerida": "Cuando hay atraso se aplica tasa de mora de 1.5x sobre la tasa regular y pueden existir restricciones segun dias en mora.",
            },
            {
                "id": 7,
                "condicion": "Usuario consulta pago anticipado",
                "respuesta_sugerida": "Puedes pagar anticipadamente sin penalidad y ahorras intereses de cuotas futuras.",
            },
            {
                "id": 8,
                "condicion": "Usuario pide cambiar refinanciar plan",
                "respuesta_sugerida": "El cambio de plan no esta disponible por este canal. Te recomiendo soporte para revisar tu caso.",
            },
            {
                "id": 9,
                "condicion": "Usuario comparte datos sensibles de pago",
                "respuesta_sugerida": "Por seguridad, no compartas datos de tarjeta, OTP o claves por chat. Usa siempre los canales seguros de pago de la app.",
            },
        ],
        "variables": [
            "primer_nombre",
            "orders",
            "account_status",
            "email",
            "phone",
        ],
    },
    "PEDIDOS": {
        "responsible_agent": "handle_operations",
        "contexto": "Order status, shipping timelines, tracking, and cancellations.",
        "pregunta": "donde esta mi pedido / estado del pedido / cuando llega / cancelar pedido",
        "keywords": "pedido, estado, seguimiento, envio, entrega, cancelacion, confirmado, en transito",
        "instrucciones": (
            "Responde con detalle de pedidos del usuario cuando exista informacion: producto, estado, fechas y siguiente accion. "
            "Usa estatus operativos: CONFIRMADO, EN PREPARACION, ENVIADO, EN TRANSITO, ENTREGADO, CANCELADO. "
            "Aclarar que tiempos de entrega se expresan en dias habiles. "
            "Si el pedido aun no llega a ENVIADO, puede cancelarse; si ya fue enviado, orientar a devolucion tras entrega. "
            "Si hay retraso despues de fecha estimada, escalar a soporte. "
            "Si no hay pedidos para el usuario, comunicarlo claramente y ofrecer ayuda para nueva compra."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Usuario con pedidos activos pregunta estado",
                "respuesta_sugerida": "Te comparto el estado actual de tu pedido y la proxima accion recomendada.",
            },
            {
                "id": 2,
                "condicion": "Pedido en CONFIRMADO o EN PREPARACION",
                "respuesta_sugerida": "Tu pedido ya fue registrado y esta siendo gestionado. Si deseas, aun podemos revisar cancelacion antes de envio.",
            },
            {
                "id": 3,
                "condicion": "Pedido ENVIADO o EN_TRANSITO",
                "respuesta_sugerida": "Tu pedido ya va en ruta. Puedes hacer seguimiento en Mis Pedidos con el numero de rastreo.",
            },
            {
                "id": 4,
                "condicion": "Pedido ENTREGADO",
                "respuesta_sugerida": "Tu pedido ya fue entregado. Si necesitas devolucion, revisamos elegibilidad segun fecha de entrega.",
            },
            {
                "id": 5,
                "condicion": "Usuario solicita cancelacion antes de ENVIADO",
                "respuesta_sugerida": "Puedes cancelar mientras el pedido no haya sido enviado. Confirmame y te guio con el proceso.",
            },
            {
                "id": 6,
                "condicion": "Usuario solicita cancelacion con pedido ENVIADO o posterior",
                "respuesta_sugerida": "Ese pedido ya fue enviado, por eso no se puede cancelar. Cuando lo recibas, te ayudo con devolucion.",
            },
            {
                "id": 7,
                "condicion": "Pedido retrasado sobre fecha estimada",
                "respuesta_sugerida": "Veo retraso frente a la fecha estimada. Este caso debe escalarse a soporte para investigacion con transportadora.",
            },
            {
                "id": 8,
                "condicion": "Usuario sin pedidos",
                "respuesta_sugerida": "No encuentro pedidos asociados en este momento. Si quieres, te ayudo a revisar productos o promociones para una nueva compra.",
            },
        ],
        "variables": [
            "primer_nombre",
            "orders",
            "delivery_address_city",
            "email_verified",
            "phone_verified",
        ],
    },
    "COMO_COMPRAR": {
        "responsible_agent": "handle_operations",
        "contexto": "Guidance for the end-to-end purchase flow in Emporyum Tech.",
        "pregunta": "como comprar / como hago una compra / pasos para comprar",
        "keywords": "comprar, checkout, carrito, confirmar compra, pago, mis pedidos",
        "instrucciones": (
            "Explica el flujo de compra de forma clara y secuencial: verificar cuenta, explorar catalogo, agregar al carrito, "
            "elegir metodo de pago, seleccionar cuotas si aplica, confirmar compra, revisar correo de confirmacion y hacer seguimiento. "
            "Si el usuario no tiene email/telefono verificado, indicar que debe verificar antes de comprar. "
            "Aclarar que los tiempos de entrega se expresan en dias habiles. "
            "Si pregunta por cancelacion, indicar que es posible antes de ENVIADO."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Usuario solicita pasos generales de compra",
                "respuesta_sugerida": "Te explico paso a paso como comprar en Emporyum Tech desde el catalogo hasta el seguimiento de entrega.",
            },
            {
                "id": 2,
                "condicion": "Usuario con verificacion incompleta",
                "respuesta_sugerida": "Antes de comprar, debes tener correo y telefono verificados para completar el proceso correctamente.",
            },
            {
                "id": 3,
                "condicion": "Usuario pregunta por cuotas durante compra",
                "respuesta_sugerida": "En checkout puedes elegir cuotas si tu compra y metodo de pago cumplen las condiciones del plan.",
            },
            {
                "id": 4,
                "condicion": "Usuario pregunta como rastrear tras compra",
                "respuesta_sugerida": "Despues de confirmar, revisa el correo y sigue tu pedido en Mis Pedidos dentro de la app.",
            },
        ],
        "variables": [
            "primer_nombre",
            "email_verified",
            "phone_verified",
            "delivery_address_city",
            "orders",
        ],
    },
    "DEVOLUCIONES": {
        "responsible_agent": "handle_returns",
        "contexto": "Returns, refund policy, eligibility checks, and escalation cases.",
        "pregunta": "quiero devolver / devolucion / reembolso / cambio de producto",
        "keywords": "devolucion, reembolso, retorno, cambio, garantia, danado, producto incorrecto",
        "instrucciones": (
            "Aplicar flujo de devolucion en dos pasos. "
            "Paso 1: validar existencia del pedido, ventana de 15 dias calendario desde entrega, y elegibilidad del producto. "
            "Paso 2: registrar motivo, confirmar solicitud, informar recoleccion (3-5 dias habiles) y reembolso (5-10 dias habiles) al mismo metodo de pago. "
            "No retornables: ropa interior, audifonos/earbuds por higiene, personalizados, perecederos, licencias digitales activadas. "
            "Si pedido no entregado aun, orientar segun estado (esperar entrega o cancelar si aplica). "
            "Escalar de inmediato: producto danado, producto incorrecto, pedido no entregado tras fecha estimada. "
            "Si piden cambio directo, explicar que no hay intercambio directo: devolucion + nueva compra."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Solicitud de devolucion sin identificar pedido",
                "respuesta_sugerida": "Claro, para iniciar necesito el numero de pedido o confirmar el pedido que quieres devolver.",
            },
            {
                "id": 2,
                "condicion": "Pedido no existe o no pertenece al usuario",
                "respuesta_sugerida": "No encontramos ese pedido asociado a tu cuenta. Verifiquemos el numero y lo revisamos.",
            },
            {
                "id": 3,
                "condicion": "Pedido fuera de ventana de 15 dias",
                "respuesta_sugerida": "El plazo de 15 dias calendario para devolucion ya vencio desde la fecha de entrega.",
            },
            {
                "id": 4,
                "condicion": "Producto no retornable",
                "respuesta_sugerida": "Ese producto no es elegible para devolucion por politica (higiene/personalizacion/tipo de producto).",
            },
            {
                "id": 5,
                "condicion": "Pedido elegible para devolucion",
                "respuesta_sugerida": "Tu pedido es elegible. Indica por favor el motivo: danado, producto diferente, no cumple expectativas, ya no lo necesito u otro.",
            },
            {
                "id": 6,
                "condicion": "Confirmacion paso 2 con motivo recibido",
                "respuesta_sugerida": "Solicitud registrada. Programaremos recoleccion en 3-5 dias habiles y el reembolso se procesa en 5-10 dias habiles tras inspeccion.",
            },
            {
                "id": 7,
                "condicion": "Caso escalable: producto danado o incorrecto",
                "respuesta_sugerida": "Lamento lo ocurrido. Este caso requiere prioridad de soporte; te guiaremos para enviar evidencia y escalar de inmediato.",
            },
            {
                "id": 8,
                "condicion": "Usuario solicita cambio directo",
                "respuesta_sugerida": "No manejamos cambio directo. Debes solicitar devolucion y luego realizar una nueva compra del producto deseado.",
            },
        ],
        "variables": [
            "primer_nombre",
            "orders",
            "delivery_address_city",
            "email",
            "phone",
        ],
    },
    "CUENTA": {
        "responsible_agent": "handle_platform",
        "contexto": "Account management, authentication, app troubleshooting, and platform/security policies.",
        "pregunta": "mi cuenta / cambiar correo / cambiar telefono / no puedo entrar / app falla",
        "keywords": "cuenta, perfil, contrasena, 2FA, bloqueada, phishing, OTP, app lenta, notificaciones",
        "instrucciones": (
            "Explica claramente que cambios son autoservicio en app y cuales requieren soporte. "
            "Autoservicio: telefono, correo, direccion, contrasena, notificaciones, 2FA. "
            "Soporte obligatorio: nombre legal, cedula, fusion de cuentas, desbloqueo por fraude. "
            "Password reset: Olvide mi contrasena y enlace al correo. "
            "Cuenta bloqueada por actividad sospechosa: escalar con verificacion de identidad. "
            "Nunca pedir OTP ni contrasenas; advertir al usuario que no comparta codigos. "
            "Para problemas de app, priorizar pasos en app (cache, update, reinicio, reinstalacion) antes de escalar. "
            "Si el dispositivo no soporta app reciente, sugerir version web."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Usuario quiere actualizar telefono o correo",
                "respuesta_sugerida": "Puedes hacerlo en Mi Perfil y completar la verificacion del nuevo dato.",
            },
            {
                "id": 2,
                "condicion": "Usuario quiere cambiar nombre legal o cedula",
                "respuesta_sugerida": "Ese cambio requiere ticket de soporte con documento de identidad; tiempo estimado 3-5 dias habiles.",
            },
            {
                "id": 3,
                "condicion": "Usuario olvido contrasena",
                "respuesta_sugerida": "Usa Olvide mi contrasena en login para recibir enlace de restablecimiento al correo registrado.",
            },
            {
                "id": 4,
                "condicion": "Usuario con cuenta bloqueada",
                "respuesta_sugerida": "Tu cuenta requiere revision por seguridad. Te recomiendo soporte para validar identidad y desbloquear.",
            },
            {
                "id": 5,
                "condicion": "Usuario consulta 2FA",
                "respuesta_sugerida": "Puedes activar autenticacion en dos pasos en Mi Perfil > Seguridad para mayor proteccion.",
            },
            {
                "id": 6,
                "condicion": "Usuario reporta app cerrandose o lenta",
                "respuesta_sugerida": "Prueba limpiar cache, actualizar app, reiniciar el celular y reinstalar si persiste.",
            },
            {
                "id": 7,
                "condicion": "Usuario no recibe notificaciones",
                "respuesta_sugerida": "Revisa permisos del telefono y ajustes en Mi Perfil > Notificaciones; en Android verifica ahorro de bateria.",
            },
            {
                "id": 8,
                "condicion": "Usuario comparte OTP o datos sensibles",
                "respuesta_sugerida": "No compartas codigos OTP ni datos sensibles por chat. Emporyum Tech nunca los solicita por este canal.",
            },
        ],
        "variables": [
            "primer_nombre",
            "email",
            "phone",
            "email_verified",
            "phone_verified",
            "account_status",
        ],
    },
    "FUERA_DE_ALCANCE": {
        "responsible_agent": "handle_general",
        "contexto": "Requests unrelated to Emporyum Tech scope.",
        "pregunta": "que hora es / quien gano el partido / temas fuera del ecommerce",
        "keywords": "fuera de alcance, no relacionado, tema externo",
        "instrucciones": (
            "Responde de forma breve y respetuosa que solo ayudas con temas de Emporyum Tech. "
            "No inventes respuestas sobre temas externos. "
            "Ofrece redireccion util hacia productos, pedidos, pagos, cuenta o devoluciones."
        ),
        "escenarios": [
            {
                "id": 1,
                "condicion": "Pregunta completamente externa",
                "respuesta_sugerida": "Solo puedo ayudarte con temas de Emporyum Tech, como pedidos, pagos, productos, cuenta o devoluciones.",
            },
            {
                "id": 2,
                "condicion": "Pregunta mixta (externa + negocio)",
                "respuesta_sugerida": "Sobre ese tema externo no tengo alcance, pero con gusto te ayudo con la parte de Emporyum Tech.",
            },
            {
                "id": 3,
                "condicion": "Usuario insiste en tema externo",
                "respuesta_sugerida": "Entiendo, pero en este canal solo puedo gestionar temas de Emporyum Tech.",
            },
            {
                "id": 4,
                "condicion": "Usuario pide alternativa",
                "respuesta_sugerida": "Si quieres, revisamos ahora mismo un pedido, tus cuotas, promociones activas o configuracion de cuenta.",
            },
        ],
        "variables": ["primer_nombre"],
    },
}

# List of all valid topic names (used by the router)
VALID_TOPICS: list = list(SCENARIO_KNOWLEDGE_BASE.keys())
