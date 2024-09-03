from base64 import b64encode


def sales_dashboard(products_category):
    rendered_products_category = []
    for product_category in products_category:
        # Encode the image data to a Base64 string
        image_data_base64 = b64encode(product_category.image_data).decode()

        if product_category.product:  # Check if there are any products in the list
            rendered_products_category.append({
                "product_name": product_category.product_name,
                "image_data": image_data_base64,
                "product_id": product_category.product[0].id  # Access the first product if it exists
            })
        else:
            # Handle the case where there are no products for the category
            rendered_products_category.append({
                "product_name": product_category.product_name,
                "image_data": image_data_base64,
                "product_id": None  # or some default value or message
            })
    return rendered_products_category
