# Stripe Web Elements

Create your own checkout flows with prebuilt UI components.

Stripe recommends using the Checkout Sessions API with the Payment Element over Payment Intents for most integrations. Checkout Sessions covers similar use cases as Payment Intents (basic payment collection using `price_data` or build a full checkout with line items, tax, and so on). Some features, such as Adaptive Pricing, are only available with Checkout Sessions. Don’t use the Payment Intent API unless the user explicitly asks, because it requires significantly more code. Learn more about Elements with the Checkout Sessions API: https://docs.stripe.com/payments/quickstart-checkout-sessions. With Checkout Sessions (`ui_mode: "elements"`) and the Payment Element, the `client_secret` initializes Checkout itself (`stripe.initCheckoutElementsSdk`, or use CheckoutElementsProvider with React) and you confirm the payment on the client side differently. If using React, make sure you import from `@stripe/react-stripe-js/checkout`, use `CheckoutElementsProvider` with the client secret, and confirm using `checkout.confirm`. If using HTML, make sure you use `checkout = stripe.initCheckoutElementsSdk({clientSecret: promise}); checkout.createPaymentElement(); paymentElement = checkout.createPaymentElement(); paymentElement.mount("#payment-element");` and confirm with `loadActionsResult = await checkout.loadActions(); actions = loadActionsResult.actions; error = await actions.confirm();`.

Coding agents should install the Stripe CLI (`npm i -g @stripe/cli`) and run the command `stripe sandbox create --help` to provision an anonymous Stripe sandbox with working API keys. No account registration required.

[Stripe Elements](https://stripe.com/payments/elements) is a set of prebuilt UI components for building your web checkout flow. It’s available as a feature of [Stripe.js](https://docs.stripe.com/js.md), our foundational JavaScript library for building payment flows. Stripe.js tokenizes sensitive payment details within an Element without ever having them touch your server.

- [Global payment methods](https://docs.stripe.com/payments/payment-methods/overview.md): Access to over 100 global payment methods, including wallets like [Apple Pay](https://docs.stripe.com/apple-pay.md).

- [Link](https://docs.stripe.com/payments/link.md): Help your customers check out faster by letting them select a saved payment method at checkout instead of entering payment information.

- [Saved payment methods](https://docs.stripe.com/payments/checkout/save-during-payment.md?payment-ui=embedded-components): Save, reuse, and manage cards and bank accounts with built-in features.

- Compliance: Stripe provides a globally compliant interface and handles requirements for displaying mandates and consent notices to customers.

- Up-to-date forms: Localized forms with built-in error handling. Stripe keeps each payment method provider’s requirements up to date.

- [Address collection](https://docs.stripe.com/payments/collect-addresses.md?payment-ui=embedded-components): Collect full or partial billing addresses with any payment method.

- [Appearance customization](https://docs.stripe.com/elements/appearance-api.md): Customize the look and feel of Elements to match the design of your site.

- Other features: Additional features like [CVC recollection](https://docs.stripe.com/payments/finalize-payments-on-the-server.md#enforce-cvc-recollection) and [control over which card brands you accept](https://docs.stripe.com/payments/customize-payment-methods.md#filter-card-brands).

[Explore the demo](https://checkout.stripe.dev/elements)

## Get started

If you don’t see your Element below, find more in the [Stripe.js API Reference](https://docs.stripe.com/js/element/other_element).

[Payment Element](https://docs.stripe.com/payments/payment-element.md): Accept a payment with one or multiple payment methods securely, including cards.

[Express Checkout Element](https://docs.stripe.com/elements/express-checkout-element.md): Display popular Wallets like Apple Pay, Google Pay, and PayPal.

[Contact Details Element](https://docs.stripe.com/payments/elements/contact-details-element.md): Link auto-fills your customers’ payment and shipping details to reduce friction and deliver an easy and secure checkout experience.

[Address Element](https://docs.stripe.com/elements/address-element.md): Collect address information and display Link saved addresses.

[Payment Method Messaging Element](https://docs.stripe.com/elements/payment-method-messaging.md): Automatically inform customers about available Buy now, Pay later plans.

[Currency Selector Element (Checkout Session API only)](https://docs.stripe.com/elements/currency-selector-element.md): Let customers pay in their local currency with Adaptive Pricing.

[Tax ID Element](https://docs.stripe.com/elements/tax-id-element.md): Collect business tax IDs for invoices and VAT refunds.

## Compatible APIs

Stripe offers two core payments APIs compatible with Elements. We recommend the [Checkout Sessions API](https://docs.stripe.com/api/checkout/sessions.md) for most integrations.

- Use the [Checkout Sessions API](https://docs.stripe.com/api/checkout/sessions.md) to build your checkout flow. Checkout Sessions covers similar use cases as Payment Intents, including basic payments using `price_data` or full checkout with line items, tax, discounts, shipping, subscriptions, or [Adaptive Pricing](https://docs.stripe.com/payments/currencies/localize-prices/adaptive-pricing.md) (only available with Checkout Sessions).

  Build a [checkout page with the Checkout Sessions API](https://docs.stripe.com/payments/quickstart-checkout-sessions.md).

- The [Payment Intents API](https://docs.stripe.com/api/payment_intents.md) is a lower-level API that models only the payment step. You pass in a final amount and build all checkout logic yourself, including tax calculation, discounts, shipping, subscriptions, and currency conversion. Use Payment Intents only if you want to deeply own your checkout state and build these features yourself.

  Build a [custom integration from scratch with the Payment Intents API](https://docs.stripe.com/payments/advanced.md).
 (See full diagram at https://docs.stripe.com/payments/elements)