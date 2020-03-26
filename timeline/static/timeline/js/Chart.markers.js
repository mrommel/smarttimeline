Chart.plugins.register({
    afterDraw: function(chartInstance) {
        if (chartInstance.config.options.markers && chartInstance.config.options.markers.display) {
            var references = chartInstance.config.options.markers.references || [];
            var helpers = Chart.helpers;
            var ctx = chartInstance.chart.ctx;
            var fontColor = helpers.getValueOrDefault(chartInstance.config.options.markers.fontColor, chartInstance.config.options.defaultFontColor);
            var fontSize = helpers.getValueOrDefault(chartInstance.config.options.markers.fontSize, Chart.defaults.global.defaultFontSize + 5);

            // render the value of the chart above the bar
            ctx.font = Chart.helpers.fontString(fontSize, 'normal', Chart.defaults.global.defaultFontFamily);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';
            ctx.fillStyle = fontColor;

            chartInstance.data.datasets.forEach(function (dataset, dsindex) {

                var meta = chartInstance.getDatasetMeta(dsindex);
                if (meta.hidden) {
                    return
                }
                //console.log('hidden: ' + meta.hidden)

                for (var i = 0; i < dataset.data.length; i++) {
                    // note, many browsers don't support the array.find() function.
                    // if you use this then be sure to provide a pollyfill
                    var refPoint = references.find(function(e) {
                        return e.datasetLabel == dataset.label && e.dataIndex === i
                    });

                    if (refPoint) {
                        var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
                        var yVal = model.y;

                        // value check
                        if (isNaN(yVal)) {
                            var beforeModel = dataset._meta[Object.keys(dataset._meta)[0]].data[i-1]._model;
                            var afterModel = dataset._meta[Object.keys(dataset._meta)[0]].data[i+2]._model;
                            yVal = (beforeModel.y + afterModel.y ) / 2.0
                        }

                        // background
                        ctx.fillStyle = 'rgba(255,255,255,1.0)';
                        ctx.strokeStyle = 'rgba(255,255,255,1.0)';
                        ctx.lineJoin = "round";
                        ctx.lineWidth = 1;

                        // triangle
                        ctx.beginPath();
                        ctx.moveTo(model.x, yVal);
                        ctx.lineTo(model.x + 7, yVal + 7);
                        ctx.lineTo(model.x - 7, yVal + 7);
                        ctx.lineTo(model.x, yVal);
                        ctx.closePath();
                        ctx.fill();

                        roundRect(ctx, model.x - 50, yVal + 7, 100, 50, 10, true);

                        var lines = refPoint.reference.split('#');
                        var lineheight = 18;
                        ctx.fillStyle = fontColor;
                        for (var j = 0; j<lines.length; j++) {
                            ctx.fillText(lines[j], model.x, yVal + 30 + (j*lineheight) );
                        }
                    }
                }
            });
        }
    }
});