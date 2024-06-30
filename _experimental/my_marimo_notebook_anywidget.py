import marimo

__generated_with = "0.6.23"
app = marimo.App(width="medium")


@app.cell
def __():
    import anywidget
    import marimo as mo
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
        # Widget front-end JavaScript code
        _esm = """
        function render({ model, el }) {
          let getCount = () => model.get("count");
          let button = document.createElement("button");
          button.innerHTML = `count is ${getCount()}`;
          button.addEventListener("click", () => {
            model.set("count", getCount() + 1);
            model.save_changes();
          });
          model.on("change:count", () => {
            button.innerHTML = `count is ${getCount()}`;
          });
          el.appendChild(button);
        }
        export default { render };
      """
        _css = """
        button {
          padding: 5px !important;
          border-radius: 5px !important;
          background-color: #f0f0f0 !important;

          &:hover {
            background-color: lightblue !important;
            color: white !important;
          }
        }
      """

        # Stateful property that can be accessed by JavaScript & Python
        count = traitlets.Int(0).tag(sync=True)

    cw = CounterWidget()
    widget = mo.ui.anywidget(cw)
    return CounterWidget, anywidget, cw, mo, traitlets, widget


@app.cell
def __(widget):
    widget
    return


@app.cell
def __(widget):
    widget.value["count"] = 19
    return


@app.cell
def __(widget):
    widget.value
    return


@app.cell
def __(cw):
    cw.count = 20
    return


@app.cell
def __(cw):
    cw.count
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
