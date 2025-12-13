
@app.route('/api/export/integrated', methods=['POST'])
def export_data_integrated_fixed():
    """تصدير البيانات المتكاملة - نسخة محسنة"""
    try:
        data = request.get_json() or {}
        export_type = data.get('type', 'products')

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        if export_type == 'products':
            query = """
                SELECT p.*, s.name as supplier_name,
                       COUNT(b.id) as batch_count,
                       COALESCE(SUM(b.الكميه_المتوافره), 0) as total_stock
                FROM products p
                LEFT JOIN suppliers s ON p.supplier_id = s.id
                LEFT JOIN batches b ON p.id = b.product_id
                GROUP BY p.id
            """
        elif export_type == 'batches':
            query = """
                SELECT b.*, p.المنتج as product_name,
                       w.name as warehouse_name,
                       s.name as supplier_name
                FROM batches b
                LEFT JOIN products p ON b.product_id = p.id
                LEFT JOIN warehouses w ON b.warehouse_id = w.id
                LEFT JOIN suppliers s ON b.supplier_id = s.id
            """
        else:
            return jsonify({'success': False,
                'error': 'نوع تصدير غير مدعوم'}),
                400

        results = conn.execute(query).fetchall()
        data_list = [dict(row) for row in results]

        conn.close()

        return jsonify({
            'success': True,
            'data': data_list,
            'count': len(data_list),
            'format': 'json',
            'message': f'تم تصدير {len(data_list)} سجل بنجاح'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'خطأ في التصدير: {str(e)}'
        }), 500
