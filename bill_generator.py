import datetime
import random

cart = []

print("=" * 50)
print("          QUICK BILL GENERATOR           ")
print("=" * 50)

# Customer Info
customer_name = input("Enter Customer Name: ").strip() or "Guest"
customer_phone = input("Enter Phone Number: ").strip() or "N/A"

# Rush Hour Premium Toggle
rush_hour_input = (
    input("\n⚡ Enable Rush Hour Premium (+10% Surge)? (y/n) [Default: n]: ")
    .strip()
    .lower()
)
is_rush_hour = rush_hour_input == "y"
surge_rate = 0.10 if is_rush_hour else 0.00

if is_rush_hour:
    print("🔥 Rush Hour Premium Active! +10% applied to product base prices.")

# Add Products Loop
while True:
    print("\n--- Add Product ---")
    name = input("Product Name (or type 'done' to finish): ").strip()
    if name.lower() == "done":
        break

    try:
        base_price = float(input("Base Price (₹): "))
        qty = int(input("Quantity: "))
        gst_rate = float(
            input("GST Rate % (e.g., 0, 5, 12, 18, 28) [Default 18]: ") or 18
        )
    except ValueError:
        print("❌ Invalid input! Price and quantity must be numbers. Try again.")
        continue

    effective_price = base_price * (1 + surge_rate)
    subtotal = effective_price * qty
    gst_amount = subtotal * (gst_rate / 100)
    total = subtotal + gst_amount

    cart.append(
        {
            "name": name,
            "base_price": base_price,
            "effective_price": effective_price,
            "qty": qty,
            "gst_rate": gst_rate,
            "gst_amount": gst_amount,
            "total": total,
        }
    )

    if is_rush_hour:
        print(
            f"✅ Added {name}! (Base: ₹{base_price:.2f} ➔ Surge Price: ₹{effective_price:.2f})"
        )
    else:
        print(f"✅ Added {name} to cart!")

if not cart:
    print("\nNo items added. Exiting program.")
else:
    try:
        discount = float(input("\nEnter Discount Amount ₹ [Default 0]: ") or 0)
    except ValueError:
        discount = 0.0

    invoice_no = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M')}-{random.randint(10, 99)}"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    gross_subtotal = sum(
        item["effective_price"] * item["qty"] for item in cart
    )
    total_gst = sum(item["gst_amount"] for item in cart)
    net_payable = max(0, (gross_subtotal + total_gst) - discount)

    rush_tag = " [RUSH HOUR SURGE APPLIED]" if is_rush_hour else ""

    bill_text = f"""
==================================================
             RETAIL STORE INVOICE            
==================================================
Invoice No : {invoice_no}
Date & Time: {now}
Customer   : {customer_name}
Phone      : {customer_phone}{rush_tag}
--------------------------------------------------
Item            Qty   Price   GST%   Total
--------------------------------------------------"""

    for item in cart:
        bill_text += f"\n{item['name'][:14]:<15} {item['qty']:<5} ₹{item['effective_price']:<6.1f} {int(item['gst_rate'])}%   ₹{item['total']:<7.2f}"

    bill_text += f"""
--------------------------------------------------
Subtotal       : ₹{gross_subtotal:.2f}
Total GST      : ₹{total_gst:.2f}
Discount       : -₹{discount:.2f}
==================================================
NET PAYABLE    : ₹{net_payable:.2f}
==================================================
        Thank you for shopping with us!
==================================================
"""

    print(bill_text)

    file_name = f"{invoice_no}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(bill_text)

    print(f"💾 Bill saved to file: {file_name}")
